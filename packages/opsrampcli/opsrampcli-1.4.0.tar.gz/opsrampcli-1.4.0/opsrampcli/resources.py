import json
import pandas as pd
import re
import xlsxwriter
from opsrampcli.opsrampenv import OpsRampEnv
from opsrampcli.DataSource import DataSource
import sys
import yaml
import logging
import importlib
import asyncio

logger = logging.getLogger(__name__)

SET_TAG_VALUE_MAX_DEVICES = 100
RESOURCE_FILE_REQUIRED_FIELDS = ['client.uniqueId', 'client.name','resourceName','resourceType']
ALL_RESOURCE_FIELDS = [
    "id",
    "name",
    "type",
    "aliasName",
    "resourceName",
    "hostName",
    "make",
    "model",
    "ipAddress",
    "alternateIpAddress",
    "os",
    "serialNumber",
    "clientId",
    "partnerId",
    "entityType",
    "nativeType",
    "dnsName",
    "moId",
    "internalId",
    "state",
    "macAddress",
    "agentInstalled",
    "monitorable",
    "tags",
    "timezone",
    "osType"
  ]

DEFAULT_RESOURCE_MAPPING_STRATEGY_OLD = {
    'name': 'Default (matching resourceType, resourceName)',
    'opsramp_fields': [
        {'fieldname': 'resourceType'},
        {'fieldname': 'resourceName'}
    ],
    'source_fields': [
        {'fieldname': 'resourceType'},
        {'fieldname': 'resourceName'}
    ]
}
    
DEFAULT_RESOURCE_MAPPING_STRATEGY_NEW = {
    'name': 'Default (matching type, name)',
    'opsramp_fields': [
        {'fieldname': 'type'},
        {'fieldname': 'name'}
    ],
    'source_fields': [
        {'fieldname': 'resourceType'},
        {'fieldname': 'resourceName'}
    ]
}
def assign_via_flattened_attribute_name(orig_object:dict, flatattr_name:str, value):
    """Given an existing dict, a flattened "dotted notation" attribute name, and a value,
       this function will update the dict with the new value in the correct location in the
       dict, including creating any missing intermediate keys.

       Args:
           orig_object: The dict to be modified
           flatattr_name: Attribute name in "flattended" dotted notation
           value: The value to be assigned
       
       Returns:
           The original dict, updated with the new value
    
    """
    if not orig_object:
        orig_object = {}

    if flatattr_name.startswith('tags.'):
        tagname = flatattr_name.split('.')[1]
        if 'tags' not in orig_object:
            orig_object['tags'] = []
        tag = {
                "name": tagname,
                "value": value,
                "metricLabel": False,
                "scope": "CLIENT"
        }
        orig_object['tags'].append(tag)
        return orig_object

    if flatattr_name.find('.') < 0:
        orig_object[flatattr_name] = value
        return orig_object
    
    attr_elements = flatattr_name.split('.')
    attrname = attr_elements.pop(0)
    if attrname in orig_object:
        subobject = orig_object[attrname]
    else:
        subobject = None
    orig_object[attrname] =  assign_via_flattened_attribute_name(subobject, ".".join(attr_elements), value)
    return orig_object


def check_if_updates(new, original):
    if type(new) == dict:
        for newkey, newvalue in new.items():
            if newkey == 'tags':
                continue
            if newkey not in original or type(newvalue) != type(original[newkey]):
                return True
            elif type(newvalue) == dict:
                if check_if_updates(newvalue, original[newkey]):
                    return True
            elif newvalue != original[newkey]:
                return True
    return False




def do_cmd_import_resources(ops: OpsRampEnv, args):
    filename = args.filename
    if not re.match(r".*\.xlsx$", filename):
        filename = filename + ".xlsx"
    df =  pd.read_excel(io=filename, engine="openpyxl", dtype=str)
    return import_resources_from_dataframe(ops, args, df)

def get_match_strategies(job:dict, old_query_type:bool=True):
    match_strategies = []
    if job and 'match_strategy' in job and job['match_strategy']:
        # Match strategy from job file
        match_strategies = job['match_strategy']
    else:
        # Default match strategy
        if old_query_type:
            match_strategies = [DEFAULT_RESOURCE_MAPPING_STRATEGY_OLD]
        else:
            match_strategies = [DEFAULT_RESOURCE_MAPPING_STRATEGY_NEW]
    return match_strategies

def build_resource_match_lookup(resources:list, match_strategies:list):
    resource_maps = []
    for strategy in match_strategies:
        map_approach = {}
        for resource in resources:
            try:
                match_string_pieces = []
                for opsramp_field in strategy['opsramp_fields']:
                    fieldval:str = resource[opsramp_field['fieldname']]
                    fieldval = fieldval.lower().strip()
                    if 'normalize' in opsramp_field and 'regex' in opsramp_field['normalize'] and 'replace' in opsramp_field['normalize']:
                        regex = opsramp_field['normalize']['regex']
                        replace = opsramp_field['normalize']['replace']
                        fieldval = re.sub(regex, replace, fieldval)
                        fieldval = fieldval.lower().strip()
                        if not fieldval:
                            logger.warn(f'When building match map of resources with approach "{strategy["name"]}": resource id {resource["id"]}, field {opsramp_field["fieldname"]} is blank so skipping the resource.')
                            raise Exception("Blank field value")
                    match_string_pieces.append(fieldval)
                match_string = "|".join(match_string_pieces)
                if match_string in map_approach:
                    logger.warn(f'When building match map of resources with approach "{strategy["name"]}": resource id {resource["id"]} duplicates already used string "{match_string}" from resource id {map_approach[match_string]} so it will be excluded from the map.')
                else:
                    map_approach[match_string] = resource['id']
            except:
                pass
        resource_maps.append(map_approach)
    return resource_maps

def build_source_match_strings(resource, match_strategies:list):
    match_strings = []
    for strategy in match_strategies:
        match_string_pieces = []
        for source_field in strategy['source_fields']:
            fieldval:str = resource[source_field['fieldname']]
            fieldval = fieldval.lower().strip()
            if 'normalize' in source_field and 'regex' in source_field['normalize'] and 'replace' in source_field['normalize']:
                regex = source_field['normalize']['regex']
                replace = source_field['normalize']['replace']
                fieldval = re.sub(regex, replace, fieldval)
                fieldval = fieldval.lower().strip()
            match_string_pieces.append(fieldval)
        match_string = "|".join(match_string_pieces)
        match_strings.append(match_string)
    return match_strings

def find_matching_resource(source_strings:list, resource_map:list, strategies:list):
    matching_resource_id = None
    if not (len(resource_map) == len(source_strings) and len(strategies) == len(source_strings)):
        logger.error(f'Length of source strings ({len(source_strings)}), resource_map ({len(resource_map)}), and strategies ({len(strategies)}) lists are not the same for saome reason - please check your job\' match_strategy section.')
        raise
    for idx,match_string in enumerate(source_strings):
        if match_string in resource_map[idx]:
            matching_resource_id = resource_map[idx][match_string]
            logger.info(f'Found matching resource id {matching_resource_id} for match string "{match_string}" using strategy #{idx+1}: {strategies[idx]["name"]}')
            break
    return matching_resource_id


async def send_missing_resource_alert(ops, args, resource):
    alert = {}
    alert['serviceName'] = "opcli_opsramp_missing_resource"
    alert['device'] = {'hostName': resource['resourceName'].lower()}
    alert['subject'] = f'Missing resource "{resource["resourceName"].lower()}" of type "{resource["resourceType"]}" detected by CMDB integration'
    alert['currentState'] = args.alertonmissing
    alert['component'] = resource["resourceType"]
    alert['description'] = f'The resource "{resource["resourceName"].lower()}" of type "{resource["resourceType"]}" exists in the CMDB but is not in OpsRamp.\nThe --nocreate option is set to {args.nocreate} and the --native_attrs_update option is set to {args.native_attrs_update}.'
    await ops.post_alert_bearer_async(alert)


def build_resource_payload(resource:pd.Series, spec:dict):
    # Build the resource create/update payload
    resource_dict = {}
    for attrname in spec['native_attrs']:
        resource_dict = assign_via_flattened_attribute_name(resource_dict, attrname, resource[attrname])
    return resource_dict


def update_existing_resource_native_attrs(ops:OpsRampEnv, resourceId, resource:pd.Series, spec:dict, existing_resource:dict):
    payload:dict = build_resource_payload(resource, spec)
    has_updated_values = check_if_updates(payload, existing_resource)
    if has_updated_values:
        response = ops.update_resource(resourceId, payload)
        if 'success' in response and response['success']:
            logger.info(f'Updated resource main attributes for name:{payload["resourceName"]} with id:{resourceId}')
        else:
            logger.error(f'Unable to update resource {payload["resourceName"]} - {response["message"]}.  Please check the data for this item.')
            return
    else:
        logger.info(f'No updates to resource main attributes name:{payload["resourceName"]} with id:{resourceId}')

def create_missing_resource_native_attrs(ops:OpsRampEnv, resource:pd.Series, spec:dict):
    payload:dict = build_resource_payload(resource, spec)
    response = ops.create_resource(payload)
    if 'resourceUUID' in response:
        resourceId = response['resourceUUID']
        logger.info(f'Created resource name:{payload["resourceName"]} with id:{resourceId}')
        return resourceId
    else:
        logger.error(f'Unable to create resource {payload["resourceName"]}.  Please check the data for this item.')
        return None
    

async def process_resource_data(ops:OpsRampEnv, args, job:dict, df:pd.DataFrame, idx, resource:pd.Series, resource_map, match_strategies, customattr_names_in_file, existing_resources_by_id, attrinfo, updateresults):
        # See if it is a new resource or already existing
        source_match_strings = build_source_match_strings(resource, match_strategies)
        resourceId = find_matching_resource(source_match_strings, resource_map, match_strategies)

        if resourceId: # Existing resource
            is_new = False
            logger.debug(f'Source record #{idx+1} {resource["resourceName"]} matches existing resource with id {resourceId} in OpsRamp')

            # Handle delete if specified
            if 'Processing Action' in resource and resource['Processing Action'] == 'Delete':
                response = ops.delete_resource(resourceId)
                logger.info(f'Deleted resource name:{resource["resourceName"]} with id:{resourceId} as its Processing Action was set to Delete')
                return
            
            # Handle native attrs update if specified
            if 'update_existing_resources' in job and job['update_existing_resources']:
                update_existing_resource_native_attrs(ops, resourceId, resource, job['update_existing_resources'], existing_resources_by_id[resourceId])


        else: # New resource
            is_new = True
            logger.info(f'Source record #{idx+1} {resource["resourceName"]} does not match any exiting resource in OpsRamp')

            if 'Processing Action' in resource and resource['Processing Action'] == 'Delete':
                    logger.warn(f'Delete action specified but there is no such resource name:{resource["resourceName"]} of specified type.')
                    return
            
            if args.alertonmisssing:
                logger.info(f"Sending a missing resource alert for source record #{idx+1}")
                send_missing_resource_alert(ops, args, resource)

            if 'create_missing_resources' in job and job['create_missing_resources']:
                resourceId = create_missing_resource_native_attrs(ops, resource, job['create_missing_resources'])
                if not resourceId:
                    return
            else:
                return


                          
        
        logger.debug(f'Processing resource-specific tags')
        for attrname in customattr_names_in_file:
            columnhead = f'tags.{attrname}'
            column = attrname
            if pd.isnull(resource[columnhead]) or pd.isna(resource[columnhead]) or resource[columnhead]=='' :
                if args.writeblanks:
                    if is_new:
                        continue
                    if "tags" in existing_resources_by_id[resourceId] and any(attr['name']==column for attr in existing_resources_by_id[resourceId]['tags']):
                        # There are one or more values and we need to remove it/them
                        remove_values = [obj['value'] for obj in existing_resources_by_id[resourceId]['tags'] if obj['name'] == column]
                        for remove_value in remove_values:
                            await ops.unset_custom_attr_on_devices_async(attrinfo[attrname]['id'], resourceId)
                        updateresults['clearsuccess'] +=1
                    else:
                        # There is already no value so nothing to remove
                        updateresults['clearskipped'] +=1
                else:
                    updateresults['clearskipped'] +=1
                    continue
            elif not is_new and "tags" in existing_resources_by_id[resourceId] and any(attr['name']==column and attr['value']==resource[columnhead] for attr in existing_resources_by_id[resourceId]['tags']):
                # It already has the same value for this attr, no need to update
                updateresults['rawresults'].append({
                    "rownum": idx+1,
                    "resourceid": resourceId,
                    "attr_name": column,
                    "attr_value": resource[columnhead],
                    "attr_id": attrinfo[attrname]['id'],
                    "attr_value_id": attrinfo[attrname]['values'][resource[columnhead]],
                    "action": "update not needed"
                })
                updateresults['updatenotneeded'] +=1
                continue
            else:
                # It has no value or a different value for this attr so we need to update

                # If it has a different value we need to remove it first
                if not is_new and "tags" in existing_resources_by_id[resourceId] and any(attr['name']==column for attr in existing_resources_by_id[resourceId]['tags']):
                    await ops.unset_custom_attr_on_devices_async(attrinfo[attrname]['id'], resourceId)

                logger.info(f'Setting tag {attrname} = {resource[columnhead]} on resource "{resource["resourceName"]}"')
                result = await ops.set_custom_attr_on_devices_async(attrinfo[attrname]['id'], attrinfo[attrname]['values'][str(resource[columnhead])], resourceId)
                updateresults['rawresults'].append({
                    "rownum": idx+1,
                    "resourceid": resourceId,
                    "attr_name": column,
                    "attr_value": resource[columnhead],
                    "attr_id": attrinfo[attrname]['id'],
                    "attr_value_id": attrinfo[attrname]['values'][str(resource[columnhead])],
                    "action": "updated"
                })
                if type(result) == list and len(result) == 1 and 'entityId' in result[0] and result[0]['entityId'] == resourceId:
                    updateresults['updatesuccess'] +=1
                else:
                    updateresults['updatefail'] +=1
                    updateresults['errors'].append({
                        "rownum": idx+1,
                        "resourceid": resourceId,
                        "attr_name": column,
                        "attr_value": resource[columnhead],
                        "attr_id": attrinfo[attrname]['id'],
                        "attr_value_id": attrinfo[attrname]['values'][str(resource[columnhead])],
                        "action": "updatefail",
                        "response": result
                    })             
async def import_resources_from_dataframe(ops: OpsRampEnv, args, df: pd.DataFrame, job: dict=None):
    logger.info(f'Getting custom attribute definitions from OpsRamp')
    customattrs = ops.get_objects(obtype="customAttributes")
    if 'code' in customattrs:
        logger.error("Error encountered retrieving custom attributes: %s" % customattrs)
        raise    

    attrinfo = {}
    for attr in customattrs:
        attrname = attr['name']
        attrinfo[attrname] = {}
        attrinfo[attrname]['id'] = attr['id']
        attrinfo[attrname]['values'] = {}

    errors = []
    logger.info('Checking source data for errors')
    for required_col in RESOURCE_FILE_REQUIRED_FIELDS:
        if required_col not in set(df.columns):
            errors.append('Required column "' + required_col + '" is missing from the spreadsheet.')
            continue
        if (len(df[df[required_col] == '']) > 0) or (len(df[pd.isna(df[required_col])]) > 0):
            errors.append('Column "' + required_col + '" has blank values which is not permitted.')
        if required_col=='name' and df['name'].duplicated().any():
            errors.append('Column "name" has duplicate values which is not permitted.')

    logger.info(f'Getting existing devices/resources from OpsRamp')
    if 'resource_opsql' in job and job['resource_opsql']:
        old_query_type = False
        opsql = job['resource_opsql']
        if 'filter' not in opsql:
            opsql['filter'] = ''
        if 'fields' not in opsql or not opsql['fields']:
            opsql['fields'] = ['id', 'name', 'resourceName', 'type', 'tags', 'os', 'ipAddress', 'serialNumber' ]
        if 'pageSize' not in opsql:
            opsql['pageSize'] = 1000

        logger.info(f'Using opsql resource search, opsql filter is \'{opsql["filter"]}\'')
        resources = ops.do_opsql_query('resource',opsql['fields'], opsql['filter'],page_size=opsql['pageSize'])
    else:
        old_query_type = True
        queryString = None
        if 'resourceType' in df:
            if len(df['resourceType'].unique()) == 1:
                rtype = df['resourceType'].unique()[0]
                queryString = f'resourceType:{rtype}'
            logger.warn(f'Using DEPRECATED old device query API, queryString is "{queryString}"')
        resources = ops.get_objects(obtype="resources", queryString=queryString, countonly=False)
        if 'code' in resources:
            logger.error("Error encountered retrieving resources: %s" % resources)
            raise    
    logger.info(f'Retrieved {len(resources)} resources from OpsRamp')
    existing_resources_by_id = {}
    for resource in resources:
        if 'resourceName' not in resource:
            resource['resourceName'] = resource['name']
        if 'resourceType' not in resource:
            resource['resourceType'] = resource['type']
        if 'name' not in resource:
            resource['name'] = resource['resourceName']
        if 'type' not in resource:
            resource['type'] = resource['resourceType']         
        existing_resources_by_id[resource['id']] = resource

    match_strategies = get_match_strategies(job, old_query_type)
    resource_map:list = build_resource_match_lookup(resources, match_strategies)

    logger.info('Getting existing tag value definitions and determining any new value definitions needing to be added')
    tag_names_to_add = []
    vals_to_add = {}
    customattr_names_in_file = []
    for columnhead in df.columns:
        df[columnhead] = df[columnhead].str.strip()
        if columnhead.startswith('tags.'):
            column = columnhead.split('.')[1]
            customattr_names_in_file.append(column)
        else:
            continue

        if column in attrinfo:
            attrvalues = ops.get_tag_values(attrinfo[column]['id'])
            for value in attrvalues:
                attrinfo[column]['values'][value['value']] = value['uniqueId']
            attrvalues_values = [obj['value'] for obj in attrvalues]
        else:
            attrvalues_values = []
            if args.addnames:
                tag_names_to_add.append(column)
            else:
                errors.append(f'Column header tags.{column} indicates a non-existent custom attribute name of {column} for the specified client.  Please create this custom attribute name in the OpsRamp UI first, or set the --addnames option to auto-add it.' )

        for val in df[columnhead].unique():
            if pd.notna(val) and val != "" and str(val) not in attrvalues_values:
                if args.addvalues:
                    strval = str(val)
                    if column not in vals_to_add:
                        vals_to_add[column] = []
                    vals_to_add[column].append(strval)
                else:
                    errors.append('Value "' + str(val) + '" specified for custom attribute "' + column + '" is not a valid value.')

    if len(errors) > 0:
        logger.error("Errors exist in the spreadsheet.  No updates to the platform have been made, please correct these errors before commiting:\n")
        for i,error in enumerate(errors):
            logger.error("%s  %s" % (str(i+1).rjust(5),error))
        #logger.error("If you want to auto-add new custom attr value definitions on the fly, use the --addvalues option otherwise undefined values will be treated as an error.\n")
        sys.exit(1)

    elif not args.commit:
        logger.info("No errors were found in the spreadsheet.  To apply the changes to the platform, rerun the command with the --commit option added.")
        sys.exit(0)

    logger.info('Preflight checks completed')
    updateresults = {
        "updatesuccess": 0,
        "updatefail": 0,
        "updatenotneeded": 0,
        "clearskipped": 0,
        "clearsuccess": 0,
        "clearfail": 0,
        "rawresults": [],
        "errors": []
    }

    logger.info(f'Adding {len(tag_names_to_add)} missing tag / custom attribute name definitions')
    for tag_name in tag_names_to_add:
        new_tag_id = ops.create_tag(tag_name)
        attrinfo[tag_name] = {}
        attrinfo[tag_name]['id'] = new_tag_id
        attrinfo[tag_name]['values'] = {}    
    
    logger.info('Adding missing tag / custom attribute value definitions')
    for column in vals_to_add.keys():
        newvalsarray = []
        for val in vals_to_add[column]:
            newvalsarray.append(val)
        ismetriclabel = False
        if job and 'tag_as_metric_label' in job and column in job['tag_as_metric_label'] and job['tag_as_metric_label'][column]:
            ismetriclabel = True
        newvals = ops.add_custom_attr_value(attrinfo[column]['id'], newvalsarray, is_metric_label=ismetriclabel)
        for value in newvals:
            attrinfo[column]['values'][value['value']] = value['id']

    # Use bulk calls for static custom attribute values
    if job and DataSource.FIELD_STATIC_VALUE in job and isinstance(job[DataSource.FIELD_STATIC_VALUE], dict):
        logger.info('Consolidating static custom attribute updates to speed things up!')
                
        for static_attr_name, static_attr_val in job[DataSource.FIELD_STATIC_VALUE].items():
            if static_attr_name.startswith("tags."):
                cleaned_static_attr_name = static_attr_name.replace("tags.","")
                resource_ids = []
                for idx,resource in df.iterrows():
                    source_match_strings = build_source_match_strings(resource, match_strategies)
                    resource_id = find_matching_resource(source_match_strings, resource_map, match_strategies)
                    if resource_id:
                        if "tags" in existing_resources_by_id[resource_id] and any(attr['name']==cleaned_static_attr_name and attr['value']==df[static_attr_name][0] for attr in existing_resources_by_id[resource_id]['tags']):
                            pass
                        else:
                            resource_ids.append(resource_id)
                number_set = 0
                number_unset = 0
                unset_coroutines = []
                set_coroutines = []
                for i in range(0, len(resource_ids), SET_TAG_VALUE_MAX_DEVICES):
                    batch = resource_ids[i:i + SET_TAG_VALUE_MAX_DEVICES]
                    unset_coroutines.append(ops.unset_custom_attr_on_devices_async(attrinfo[cleaned_static_attr_name]['id'], batch))
                    number_unset += len(batch)
                await asyncio.gather(*unset_coroutines)
                logger.info(f'Bulk unset static attribute "{cleaned_static_attr_name}" for {number_unset} resources.')

                for i in range(0, len(resource_ids), SET_TAG_VALUE_MAX_DEVICES):
                    batch = resource_ids[i:i + SET_TAG_VALUE_MAX_DEVICES]
                    set_coroutines.append(ops.set_custom_attr_on_devices_async(attrinfo[cleaned_static_attr_name]['id'], attrinfo[cleaned_static_attr_name]['values'][str(df[static_attr_name][0])], batch, False))
                    number_set += len(batch)
                await asyncio.gather(*set_coroutines)
                logger.info(f'Bulk set static attribute "{cleaned_static_attr_name}" to value "{str(df[static_attr_name][0])}" for {number_set} resources.')

                df = df.drop(columns=[static_attr_name])
                customattr_names_in_file.remove(cleaned_static_attr_name)
                
        logger.info(f'Finished consolidated bulk update of static custom attribute values!')

    logger.info('Processing per-resource values')
    for idx,resource in df.iterrows():
        logger.debug(f'Processing per-resource values for source record #{idx+1} of {len(df.index)} named {resource["resourceName"]} of type {resource["resourceType"]}')
        await process_resource_data(ops, args, job, df, idx, resource, resource_map, match_strategies, customattr_names_in_file, existing_resources_by_id, attrinfo, updateresults)
    logger.info("Completed processing all resources.") 

def do_cmd_get_resources(ops,args):
    if args.search:
        if args.count:
            aggregate="count"
            groupBy = []
            fields = None
        else:
            aggregate=None
            groupBy=None
            fields = ALL_RESOURCE_FIELDS

        result = ops.do_opsql_query("resource", fields, args.search, aggregate, groupBy)
        if args.count:
            result = result[0]["count"]
    else:
        result = ops.get_objects(obtype="resources", queryString=args.query, countonly=args.count)

    if args.delete:
        confirm_delete = 'NO'
        confirm_delete = input(f'This will result in the deletion of {len(result)} resources.  Enter YES (upper case) to confirm deletion or enter anything else to just print a list of the resources that would be deleted: ')
    
        if confirm_delete == 'YES':
            for (idx, resource) in enumerate(result):
                if "resourceType" not in resource:
                    if "type" in resource:
                        resource["resourceType"] = resource["type"]
                    else:
                        resource["resourceType"] = "NONE"
                logger.info(f'Deleting resource #{idx+1} - {resource["name"]} ({resource["resourceType"]}) with uniqueId {resource["id"]}')
                try:
                    logger.info(ops.delete_resource(resource['id']))
                except Exception as e:
                    logger.error(f'Error ocurred deleting ressource with id {resource["id"]}', exc_info=e)
        else:
            return result

    elif args.manage:
        confirm_manage = 'NO'
        confirm_manage = input(f'This will result in managing {len(result)} resources.  Enter YES (upper case) to confirm or enter anything else to just print a list of the resources that would be managed: ')
    
        if confirm_manage == 'YES':
            for (idx, resource) in enumerate(result):
                logger.info(f'Managing resource #{idx+1} - {resource["name"]}')
                try:
                    logger.info(ops.do_resource_action("manage", resource['id']))
                except Exception as e:
                    logger.error(f'Exception occurred attempting to manage resource {resource["name"]} with id {resource["id"]}', exc_info=e)

        else:
            return result      


    else:
         return result

async def do_cmd_importfromdatasource(ops, args):

    with open(args.job, 'r') as jobfile:
        job = yaml.safe_load(jobfile)
        sourcename:str = list(job['source'])[0]
        if sourcename.lower() == 'servicenow':
            modulename = 'opsrampcli.ServiceNowDataSource'
            classname = 'ServiceNowDataSource'
        elif sourcename.lower() == 'urlsource':
            modulename = 'opsrampcli.URLDataSource'
            classname = 'URLDataSource'

        sourcemodule = importlib.import_module(modulename)
        sourceclass = getattr(sourcemodule, classname)

        source:DataSource = sourceclass(job)

        logger.info(f'Querying resources from datasource: {classname}')
        df = source.get_data_from_source()
        logger.info(f'Retrieved {len(df.index)} resources from datasource: {classname}')
        return await import_resources_from_dataframe(ops, args, df, job)