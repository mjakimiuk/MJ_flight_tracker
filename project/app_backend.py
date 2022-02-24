import os
from collections import namedtuple
from typing import Dict

import airportsdata
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests_html import HTMLSession
from sqlalchemy import create_engine
from sqlalchemy.types import Float, Integer, Text

# Load environment variables. Environment variables are stored in .env file
# where sensitive data is kept. This file is ignored by git on purpose.
load_dotenv()


# Module constants
API_BASE = "http://airlabs.co/api/v9/"


def airlabs_airlines_response_data() -> Dict:
    """
    Function retrieves airlines name database in json dictionary format.
    """
    params = {
        "api_key": os.environ[
            "AIRLABS_API_KEY"
        ],  # API personal key, for testing purpose I will leave it
        "name": "",  # Get results sorted by name
    }
    method = "airlines"  # One of AIRLABS API's databases
    api_result = requests.get(API_BASE + method, params)
    api_response = api_result.json()
    return api_response["response"]


def airlabs_airlines_data_into_sql():
    """
    Function transforms .json data from AIRLABS_airlines_response_data()
    function to Pandas Dataframe. Dataframe is then sent to SQL database
    """
    engine = create_engine(
        os.environ["CONNECTION_LINK"], echo=True
    )  # Database personal key
    dataframe = pd.DataFrame.from_dict(airlabs_airlines_response_data())
    dataframe.to_sql(
        "airlines_database",
        engine,
        if_exists="replace",
        index=True,
        chunksize=500,
        dtype={
            "index": Integer,
            "icao_code": Text,
            "iata_code": Text,
            "name": Text,
        },
    )


def airlabs_flights_response_data(departure, arrival) -> Dict:
    """
    Function retrieves flights data database in json dictionary format.
    """
    params = {
        "api_key": os.environ["AIRLABS_API_KEY"],  # API personal key
        "dep_iata": departure,
        "arr_iata": arrival,
    }
    method = "flights"  # One of AIRLABS API's databases
    api_result = requests.get(API_BASE + method, params)
    api_response = api_result.json()
    return api_response["response"]


def airlabs_flights_data_into_sql(departure, arrival):
    """
    Function transforms .json data from AIRLABS_flights_response_data()
    function to Pandas Dataframe. Dataframe is then sent to SQL database
    """
    engine = create_engine(
        os.environ["CONNECTION_LINK"], echo=True
    )  # Database personal key
    dataframe = pd.DataFrame.from_dict(
        airlabs_flights_response_data(departure, arrival)
    )
    dataframe.to_sql(
        "flights_database",
        engine,
        if_exists="replace",
        index=True,
        chunksize=500,
        dtype={
            "index": Integer,
            "aircraft_icao": Text,
            "airline_iata": Text,
            "airline_icao": Text,
            "alt": Integer,
            "arr_iata": Text,
            "dep_iata": Text,
            "dir": Integer,
            "flag": Text,
            "flight_iata": Text,
            "flight_icao": Text,
            "flight_number": Text,
            "hex": Text,
            "lat": Float,
            "lng": Float,
            "reg_number": Text,
            "speed": Integer,
            "squawk": Text,
            "status": Text,
            "updated": Integer,
            "v_speed": Float,
        },
    )


def airlabs_schedules_response_data(departure, arrival) -> Dict:
    """
    Function retrieves flight schedules database for
    specific airport in json dictionary format.
    """
    params = {
        "api_key": os.environ["AIRLABS_API_KEY"],  # API personal key
        "dep_iata": departure,
        "arr_iata": arrival,
    }
    method = "schedules"  # One of AIRLABS API's databases
    api_result = requests.get(API_BASE + method, params)
    api_response = api_result.json()
    return api_response["response"]


def airlabs_schedules_data_into_sql(departure, arrival):
    """
    Function transforms .json data from AIRLABS_airlines_response_data()
    function to Pandas Dataframe. Dataframe is then sent to SQL database
    """
    engine = create_engine(
        os.environ["CONNECTION_LINK"], echo=True
    )  # Database personal key
    dataframe = pd.DataFrame.from_dict(
        airlabs_schedules_response_data(departure, arrival)
    )
    dataframe.to_sql(
        "schedules_database",
        engine,
        if_exists="replace",
        index=True,
        chunksize=500,
        dtype={
            "index": Integer,
            "aircraft_icao": Text,
            "airline_iata": Text,
            "airline_icao": Text,
            "arr_baggage": Text,
            # "arr_estimated":  Text,
            # "arr_estimated_ts":  Text,
            # "arr_estimated_utc":  Text,
            "arr_gate": Text,
            "arr_iata": Text,
            "arr_icao": Text,
            "arr_terminal": Text,
            "arr_time": Text,
            "arr_time_ts": Text,
            "arr_time_utc": Text,
            "cs_airline_iata": Text,
            "cs_flight_iata": Text,
            "cs_flight_number": Text,
            "delayed": Integer,
            # "dep_actual":  Text,
            # "dep_actual_ts":  Text,
            # "dep_actual_utc":  Text,
            # "dep_estimated":  Text,
            # "dep_estimated_ts":  Text,
            # "dep_estimated_utc":  Text,
            "dep_gate": Text,
            "dep_iata": Text,
            "dep_icao": Text,
            "dep_terminal": Text,
            "dep_time": Text,
            "dep_time_ts": Text,
            "dep_time_utc": Text,
            "duration": Text,
            "flight_iata": Text,
            "flight_icao": Text,
            "flight_number": Text,
            "status": Text,
        },
    )


def airports_module_dataframe():
    """
    Function uses aiportsdata module to retrieve
    dataframe with airports names and IATA codes.
    """
    airports = airportsdata.load()
    dataframe_base = pd.DataFrame.from_dict(airports, orient="index")
    dataframe_base["iata"].replace(
        "", np.nan, inplace=True
    )  # replace empty cells with NaN
    dataframe_new = dataframe_base[["iata", "name", "city"]].dropna(
        thresh=3
    )  # drop cells with NaN value
    dataframe_new["name_city"] = dataframe_new[["name", "city"]].agg(
        " - ".join, axis=1
    )  # 3rd column added with Airport name + City Name
    return dataframe_new


def airports_data_into_sql():
    """
    Function transforms dataframe into SQL table.
    """
    engine = create_engine(
        os.environ["CONNECTION_LINK"], echo=True
    )  # Database personal key
    dataframe = pd.DataFrame.from_dict(airports_module_dataframe())
    dataframe.to_sql(
        "airport_database_table",
        engine,
        if_exists="replace",
        index=True,
        chunksize=500,
        dtype={
            "index": Text,
            "iata": Text,
            "name": Text,
            "city": Text,
            "name_city": Text,
        },
    )


def flight_dep_arr_actual(flight_number):
    Flight = namedtuple("Flight", ["departure", "arrival"])
    if flight_number is None:
        F = Flight("no data", "no data")
        return F
    text = flight_number
    session = HTMLSession()
    response = session.get("https://www.google.com/search?q=" + text + "+flight")
    soup = BeautifulSoup(response.content, "lxml")
    actual_time = soup.find_all("div", {"class": "KUI09c Efa9ze"})
    if not actual_time:
        actual_time = soup.find_all("div", {"class": "KUI09c KskRob"})
    if not actual_time:
        F = Flight("no data", "no data")
        return F
    scraped_data = [i.text for i in actual_time[0:2]]
    F = Flight(scraped_data[0], scraped_data[1])
    return F


if __name__ == "__main__":
    airports_data_into_sql()