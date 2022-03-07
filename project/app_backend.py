from typing import Dict

import airportsdata
import requests

from .config import AIRLABS_API_KEY, API_BASE
from .db import session
from .models import Airlines, Airport, Schedules

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
    for airline in airlines:
        session.add(
            Airlines(
                icao_code=airline["icao_code"]
                if airline.get("icao_code")
                else "no data",
                iata_code=airline["iata_code"]
                if airline.get("iata_code")
                else "no data",
                name=airline["name"] if airline.get("name") else "no data",
            )
        )
    session.commit()


def _airlabs_flights_response_data(departure, arrival) -> Dict:
    """
    Function retrieves flights data database in json dictionary format.
    """
    params = {
        "api_key": AIRLABS_API_KEY,
        "dep_iata": departure,
        "arr_iata": arrival,
    }
    method = "flights"
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
        "api_key": AIRLABS_API_KEY,
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
    if not schedules:
        return False
    session.query(Schedules).delete()
    for flights in schedules:

        session.add(
            Schedules(
                aircraft_icao=flights["aircraft_icao"]
                if flights.get("aircraft_icao")
                else "-",
                airline_iata=flights["airline_iata"]
                if flights.get("airline_iata")
                else "-",
                airline_icao=flights["airline_icao"]
                if flights.get("airline_icao")
                else "-",
                arr_baggage=flights["arr_baggage"]
                if flights.get("arr_baggage")
                else "-",
                arr_estimated=flights["arr_estimated"]
                if flights.get("arr_estimated")
                else "-",
                arr_estimated_ts=flights["arr_estimated_ts"]
                if flights.get("arr_estimated_ts")
                else "-",
                arr_estimated_utc=flights["arr_estimated_utc"]
                if flights.get("arr_estimated_utc")
                else "-",
                arr_gate=flights["arr_gate"] if flights.get("arr_gate") else "-",
                arr_iata=flights["arr_iata"] if flights.get("arr_iata") else "-",
                arr_icao=flights["arr_icao"] if flights.get("arr_icao") else "-",
                arr_terminal=flights["arr_terminal"]
                if flights.get("arr_terminal")
                else "-",
                arr_time=flights["arr_time"] if flights.get("arr_time") else "-",
                arr_time_ts=flights["arr_time_ts"]
                if flights.get("arr_time_ts")
                else "-",
                arr_time_utc=flights["arr_time_utc"]
                if flights.get("arr_time_utc")
                else "-",
                cs_airline_iata=flights["cs_airline_iata"]
                if flights.get("cs_airline_iata")
                else "-",
                cs_flight_iata=flights["cs_flight_iata"]
                if flights.get("cs_flight_iata")
                else "-",
                cs_flight_number=flights["cs_flight_number"]
                if flights.get("cs_flight_number")
                else "-",
                delayed=flights["delayed"] if flights.get("delayed") else "-",
                dep_actual=flights["dep_actual"] if flights.get("dep_actual") else "-",
                dep_actual_ts=flights["dep_actual_ts"]
                if flights.get("dep_actual_ts")
                else "-",
                dep_actual_utc=flights["dep_actual_utc"]
                if flights.get("dep_actual_utc")
                else "-",
                dep_estimated=flights["dep_estimated"]
                if flights.get("dep_estimated")
                else "-",
                dep_estimated_ts=flights["dep_estimated_ts"]
                if flights.get("dep_estimated_ts")
                else "-",
                dep_estimated_utc=flights["dep_estimated_utc"]
                if flights.get("dep_estimated_utc")
                else "-",
                dep_gate=flights["dep_gate"] if flights.get("dep_gate") else "-",
                dep_iata=flights["dep_iata"] if flights.get("dep_iata") else "-",
                dep_icao=flights["dep_icao"] if flights.get("dep_icao") else "-",
                dep_terminal=flights["dep_terminal"]
                if flights.get("dep_terminal")
                else "-",
                dep_time=flights["dep_time"] if flights.get("dep_time") else "-",
                dep_time_ts=flights["dep_time_ts"]
                if flights.get("dep_time_ts")
                else "-",
                dep_time_utc=flights["dep_time_utc"]
                if flights.get("dep_time_utc")
                else "-",
                duration=flights["duration"] if flights.get("duration") else "-",
                flight_iata=flights["flight_iata"]
                if flights.get("flight_iata")
                else "-",
                flight_icao=flights["flight_icao"]
                if flights.get("flight_icao")
                else "-",
                flight_number=flights["flight_number"]
                if flights.get("flight_number")
                else "-",
                status=flights["status"] if flights.get("status") else "-",
            )
        )
    session.commit()


def airports_data_into_sql():
    """
    Function that imports airports
    """
    airports = airportsdata.load()
    for airport in airports.values():
        if airport["iata"]:
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
    # airports_data_into_sql()
    # airlabs_schedules_data_into_sql("BGO",'OSL')
    airlabs_airlines_data_into_sql()
    airports_data_into_sql()
