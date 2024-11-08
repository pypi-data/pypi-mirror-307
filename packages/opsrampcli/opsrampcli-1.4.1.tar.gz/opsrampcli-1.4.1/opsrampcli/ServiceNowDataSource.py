import requests
from opsrampcli.DataSource import DataSource
import pandas as pd
from datetime import datetime
import pytz
import os
import logging

logger = logging.getLogger(__name__)


class ServiceNowDataSource(DataSource):
    SERVICENOW_DISPLAY_VALUE = 'display_value'

    class SnowDataSourceException(DataSource.DataSourceException):
        pass

    def get_resources_df(self):
        job = self.job
        instance_url = os.getenv("SERVICENOW_URL") or job['source']['servicenow']['instance_url']
        url = instance_url + f"/api/now/table/{job['source']['servicenow']['table']}"

        user = os.getenv("SERVICENOW_USER") or job['source']['servicenow']['auth']['username']
        password = os.getenv("SERVICENOW_PASSWORD") or job['source']['servicenow']['auth']['password']
        auth = requests.auth.HTTPBasicAuth(user, password)
        qstrings = {}
        for k, v in job['source']['servicenow']['query_parameters'].items():
            qstrings[f'sysparm_{k}'] = v
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.get(url=url, auth=auth, params=qstrings, headers=headers)
        try:
            responsedict = response.json()
        except Exception as e:
            msg = f'Failed to retrieve records from ServiceNow datasource: {e}, {response.text}'
            raise ServiceNowDataSource.SnowDataSourceException(msg)
        records = responsedict.get('result', [])
        processed_recs = []
        for record in records:
            newrec = {}
            for key,value in record.items():
                if isinstance(value, dict) and ServiceNowDataSource.SERVICENOW_DISPLAY_VALUE in value:
                    newrec[key] = value[ServiceNowDataSource.SERVICENOW_DISPLAY_VALUE]
                else:
                    newrec[key] = value
            processed_recs.append(newrec)

        self.df = pd.DataFrame(processed_recs)

