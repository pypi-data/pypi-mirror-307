import requests
from requests_ntlm import HttpNtlmAuth
import pandas as pd
import os
import logging
from opsrampcli.DataSource import DataSource

logger = logging.getLogger(__name__)

URLSOURCE_DISPLAY_VALUE = 'display_value'


class URLDataSource(DataSource):

    class URLDataSourceException(DataSource.DataSourceException):
        pass

    def get_resources_df(self):
        job = self.job
        url = os.getenv("URLSOURCE_URL") or job['source']['urlsource']['url']

        user = os.getenv("URLSOURCE_USER") or job['source']['urlsource']['auth']['username']
        password = os.getenv("URLSOURCE_PASSWORD") or job['source']['urlsource']['auth']['password']
        result_key = os.getenv("URLSOURCE_RESULT_KEY") or job['source']['urlsource']['result_key'] or 'result'
       
        if 'ssl_verify' in job['source']['urlsource'] and job['source']['urlsource']['ssl_verify'] == False:
            ssl_verify = False
        else:
            ssl_verify = True

        if job['source']['urlsource']['auth']['type'] == 'basic':
            auth = requests.auth.HTTPBasicAuth(user, password)
        elif job['source']['urlsource']['auth']['type'] == 'ntlm':
            auth = HttpNtlmAuth(user, password)

        qstrings = {}
        for k, v in job['source']['urlsource']['query_parameters'].items():
            qstrings[f'{k}'] = v
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        if 'headers' in job['source']['urlsource'] and job['source']['urlsource']['headers']:
            headers = job['source']['urlsource']['headers']
        response = requests.get(url=url, auth=auth, params=qstrings, headers=headers, verify=ssl_verify)
        try:
            responsedict = response.json()
        except Exception as e:
            msg = f'Failed to retrieve records from URL datasource: {e}'
            raise URLDataSource.URLDataSourceException(msg)
        records = responsedict.get(result_key, [])
        processed_recs = []
        for record in records:
            newrec = {}
            for key,value in record.items():
                if isinstance(value, dict) and URLSOURCE_DISPLAY_VALUE in value:
                    newrec[key] = value[URLSOURCE_DISPLAY_VALUE]
                else:
                    newrec[key] = value
            processed_recs.append(newrec)

        self.df = pd.DataFrame(processed_recs)
        self.df.fillna("", inplace=True)
