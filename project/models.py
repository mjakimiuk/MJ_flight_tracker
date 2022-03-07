from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))
    api_key = Column(String(1000))


class Airport(Base):
    __tablename__ = "airport"
    id = Column(Integer, primary_key=True)
    city = Column(String(100), unique=False, nullable=False)
    country = Column(String(100), unique=False, nullable=False)
    iata = Column(String(100), unique=False, nullable=False)
    icao = Column(String(100), unique=False, nullable=False)
    name = Column(String(100), unique=False, nullable=False)


class Schedules(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    aircraft_icao = Column(String(100), unique=False, nullable=False)
    airline_iata = Column(String(100), unique=False, nullable=False)
    airline_icao = Column(String(100), unique=False, nullable=False)
    arr_baggage = Column(String(100), unique=False, nullable=False)
    arr_estimated = Column(String(100), unique=False, nullable=False)
    arr_estimated_ts = Column(String(100), unique=False, nullable=False)
    arr_estimated_utc = Column(String(100), unique=False, nullable=False)
    arr_gate = Column(String(100), unique=False, nullable=False)
    arr_iata = Column(String(100), unique=False, nullable=False)
    arr_icao = Column(String(100), unique=False, nullable=False)
    arr_terminal = Column(String(100), unique=False, nullable=False)
    arr_time = Column(String(100), unique=False, nullable=False)
    arr_time_ts = Column(String(100), unique=False, nullable=False)
    arr_time_utc = Column(String(100), unique=False, nullable=False)
    cs_airline_iata = Column(String(100), unique=False, nullable=False)
    cs_flight_iata = Column(String(100), unique=False, nullable=False)
    cs_flight_number = Column(String(100), unique=False, nullable=False)
    delayed = Column(String(100), unique=False, nullable=False)
    dep_actual = Column(String(100), unique=False, nullable=False)
    dep_actual_ts = Column(String(100), unique=False, nullable=False)
    dep_actual_utc = Column(String(100), unique=False, nullable=False)
    dep_estimated = Column(String(100), unique=False, nullable=False)
    dep_estimated_ts = Column(String(100), unique=False, nullable=False)
    dep_estimated_utc = Column(String(100), unique=False, nullable=False)
    dep_gate = Column(String(100), unique=False, nullable=False)
    dep_iata = Column(String(100), unique=False, nullable=False)
    dep_icao = Column(String(100), unique=False, nullable=False)
    dep_terminal = Column(String(100), unique=False, nullable=False)
    dep_time = Column(String(100), unique=False, nullable=False)
    dep_time_ts = Column(String(100), unique=False, nullable=False)
    dep_time_utc = Column(String(100), unique=False, nullable=False)
    duration = Column(String(100), unique=False, nullable=False)
    flight_iata = Column(String(100), unique=False, nullable=False)
    flight_icao = Column(String(100), unique=False, nullable=False)
    flight_number = Column(String(100), unique=False, nullable=False)
    status = Column(String(100), unique=False, nullable=False)


class Airlines(Base):
    __tablename__ = "airlines"
    id = Column(Integer, primary_key=True)
    icao_code = Column(String(100), unique=False, nullable=False)
    iata_code = Column(String(100), unique=False, nullable=False)
    name = Column(String(100), unique=False, nullable=False)
