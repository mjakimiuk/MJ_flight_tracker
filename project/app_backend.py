from typing import Dict

import airportsdata
import requests

from .config import AIRLABS_API_KEY, API_BASE
from .db import session
from .models import Airport

MAX_THREADS = 30


def _airlabs_airlines_response_data() -> Dict:
    """
    Function retrieves airlines name database in json dictionary format.
    """
    params = {
        "api_key": AIRLABS_API_KEY,
        "name": "",  # Get results sorted by name
    }
    method = "airlines"  # One of AIRLABS API's databases
    api_result = requests.get(API_BASE + method, params)
    api_response = api_result.json()
    return api_response["response"]


def airlabs_airlines_data_into_sql():
    """
    Function to import airlines
    """
    airlines = _airlabs_airlines_response_data()
    breakpoint()


def _airlabs_flights_response_data(departure, arrival) -> Dict:
    """
    Function retrieves flights data database in json dictionary format.
    """
    params = {
        "api_key": AIRLABS_API_KEY,
        "dep_iata": departure,
        "arr_iata": arrival,
    }
    method = "flights"  # One of AIRLABS API's databases
    api_result = requests.get(API_BASE + method, params)
    api_response = api_result.json()
    return api_response["response"]


def airlabs_flights_data_into_sql(departure, arrival):
    """
    Function to import flights
    """
    flights = _airlabs_flights_response_data(departure, arrival)
    breakpoint()


def airlabs_schedules_response_data(departure, arrival) -> Dict:
    """
    Function retrieves flight schedules database for
    specific airport in json dictionary format.
    """
    params = {
        "api_key": AIRLABS_API_KEY,  # API personal key
        "dep_iata": departure,
        "arr_iata": arrival,
    }
    method = "schedules"  # One of AIRLABS API's databases
    api_result = requests.get(API_BASE + method, params)
    api_response = api_result.json()
    return api_response["response"]


def airlabs_schedules_data_into_sql(departure, arrival):
    """
    Function to import schedules
    """
    schedules = airlabs_schedules_response_data(departure, arrival)
    breakpoint()


def airports_data_into_sql():
    """
    Function that imports airports
    """
    airports = airportsdata.load()
    for airport in airports.values():
        session.add(
            Airport(
                city=airport["city"],
                country=airport["country"],
                iata=airport["iata"],
                icao=airport["icao"],
                name=airport["name"],
            )
        )
    session.commit()


if __name__ == "__main__":
    airports_data_into_sql()
