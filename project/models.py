from . import db
from flask_login import UserMixin

class User_Table(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Airport_database(db.Model):  # SQLalchemy model
    __tablename__ = 'airport_database_table'
    index = db.Column(db.String(100), unique=False, nullable=False, primary_key=True)
    iata = db.Column(db.String(100), unique=False, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    city = db.Column(db.String(100), unique=False, nullable=False)
    name_city = db.Column(db.String(100), unique=False, nullable=False)

class Airport_Schedules_database(db.Model):  # SQLalchemy model
    __tablename__ = 'schedules_database'
    index = db.Column(db.String(100), unique=False, nullable=False, primary_key=True)
    aircraft_icao = db.Column(db.String(100), unique=False, nullable=False)
    airline_iata = db.Column(db.String(100), unique=False, nullable=False)
    airline_icao = db.Column(db.String(100), unique=False, nullable=False)
    arr_baggage = db.Column(db.String(100), unique=False, nullable=False)
    #arr_estimated = db.Column(db.String(100), unique=False, nullable=False)
    #arr_estimated_ts = db.Column(db.String(100), unique=False, nullable=False)
    #arr_estimated_utc = db.Column(db.String(100), unique=False, nullable=False)
    arr_gate = db.Column(db.String(100), unique=False, nullable=False)
    arr_iata = db.Column(db.String(100), unique=False, nullable=False)
    arr_icao = db.Column(db.String(100), unique=False, nullable=False)
    arr_terminal = db.Column(db.String(100), unique=False, nullable=False)
    arr_time = db.Column(db.String(100), unique=False, nullable=False)
    arr_time_ts = db.Column(db.String(100), unique=False, nullable=False)
    arr_time_utc = db.Column(db.String(100), unique=False, nullable=False)
    cs_airline_iata = db.Column(db.String(100), unique=False, nullable=False)
    cs_flight_iata = db.Column(db.String(100), unique=False, nullable=False)
    cs_flight_number = db.Column(db.String(100), unique=False, nullable=False)
    delayed = db.Column(db.String(100), unique=False, nullable=False)
    #dep_actual = db.Column(db.String(100), unique=False, nullable=False)
    #dep_actual_ts = db.Column(db.String(100), unique=False, nullable=False)
    #dep_actual_utc = db.Column(db.String(100), unique=False, nullable=False)
    #dep_estimated = db.Column(db.String(100), unique=False, nullable=False)
    #dep_estimated_ts = db.Column(db.String(100), unique=False, nullable=False)
    #dep_estimated_utc = db.Column(db.String(100), unique=False, nullable=False)
    dep_gate = db.Column(db.String(100), unique=False, nullable=False)
    dep_iata = db.Column(db.String(100), unique=False, nullable=False)
    dep_icao = db.Column(db.String(100), unique=False, nullable=False)
    dep_terminal = db.Column(db.String(100), unique=False, nullable=False)
    dep_time = db.Column(db.String(100), unique=False, nullable=False)
    dep_time_ts = db.Column(db.String(100), unique=False, nullable=False)
    dep_time_utc = db.Column(db.String(100), unique=False, nullable=False)
    duration = db.Column(db.String(100), unique=False, nullable=False)
    flight_iata = db.Column(db.String(100), unique=False, nullable=False)
    flight_icao = db.Column(db.String(100), unique=False, nullable=False)
    flight_number = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.String(100), unique=False, nullable=False)