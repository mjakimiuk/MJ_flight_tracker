from typing import Dict
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text


def AIRLABS_airlines_response_data() -> Dict:
    """
    Function retrieves airlines name databes in json dictionary format.
    """
    params = {
    'api_key': '0b811789-1183-4a07-804b-1fa64fc83e77',  # API personal key, for testing purpose I will leave it
    'name': ''  # Get results sorted by name
    }
    method = 'airlines'  # One of AIRLABS API's databases
    api_base = 'http://airlabs.co/api/v9/'
    api_result = requests.get(api_base+method, params)
    api_response = api_result.json()
    return api_response['response']


def AIRLABS_data_into_sql():
    """
    Function transforms .json data from AIRLABS_airlines_response_data() function to Pandas Dataframe.
    Dataframe is then sent to SQL database
    """
    engine = create_engine('postgresql+psycopg2://postgres:MarJak12!@172.19.112.1/airports', echo=True)  # API personal key, for testing purpose I will leave it
    dataframe = pd.DataFrame.from_dict(AIRLABS_airlines_response_data())
    dataframe.to_sql(
                    'airlines_database',
                    engine,
                    if_exists='replace',
                    index=True,
                    chunksize=500,
                    dtype={
                        "index": Integer,
                        "icao_code": Text,
                        "iata_code": Text,
                        "name":  Text,
                        }
                    )


if __name__ == '__main__':
    AIRLABS_data_into_sql()

