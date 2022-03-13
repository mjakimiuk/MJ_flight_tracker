from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from . import db
from .app_backend import (
    airlabs_schedules_data_into_sql,
    decrypt_api_code,
    encrypt_api_code,
)
from .models import Airlines, Airport, Schedules, User

# from .sendgrid_app import send_email_sendgrid

main = Blueprint("main", __name__)

headings = (
    "Index",
    "Departure",
    "Estimated Departure",
    "Flight",
    "Airline",
    "Departure gate",
    "Departure terminal",
    "Arrival gate",
    "Arrival terminal",
    "Baggage belt",
    "Arrival",
    "Estimated Arrival",
    "Delayed",
    "Duration",
    "Status",
    "Follow flight",
)


@main.route("/")
@login_required
def index():

    database_data = db.session.query(Airport).all()
    airports = {
        f"{i.iata} {i.city}" + f" {i.name}".replace(i.city, "") for i in database_data
    }
    return render_template("index.html", name=current_user.name, airports=airports)


@main.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    api_key_stored = ""
    api_key = request.form.get("api_key")
    user = db.session.query(User).filter_by(email=current_user.email).first()
    if api_key:

        user.api_key = encrypt_api_code(api_key)
        db.session.commit()
    if user.api_key:
        api_key_stored = decrypt_api_code(user.api_key)
        if request.method == "POST" and "api_key_resubmit" in request.form:
            api_key_stored = ""
    return render_template(
        "profile.html", name=current_user.name, api_key=api_key_stored
    )


@main.route("/flights", methods=["POST", "GET"])
@login_required
def flights():
    departure = (
        db.session.query(Airport)
        .filter(Airport.iata == request.form.get("airport_1").split()[0])
        .first()
    )
    arrival = (
        db.session.query(Airport)
        .filter(Airport.iata == request.form.get("airport_2").split()[0])
        .first()
    )
    no_data = ""
    if airlabs_schedules_data_into_sql(departure.iata, arrival.iata) is False:
        no_data = "No Data"
        data_in_table = "No Data"
        destination_tuple = "No Data"
    else:
        airlabs_schedules_data_into_sql(departure.iata, arrival.iata)
        database_data = db.session.query(Schedules).all()
        airline_names_codes = [i.airline_icao for i in database_data]
        airline_names = db.session.query(Airlines).filter(
            Airlines.icao_code.in_(airline_names_codes)
        )
        airline_names_list = {i.icao_code: i.name for i in airline_names}
        destination_tuple = (
            request.form.get("airport_1"),
            request.form.get("airport_2"),
        )
        user = db.session.query(User).filter_by(email=current_user.email).first()
        database_data_by_user = (
            db.session.query(Schedules)
            .filter_by(
                parent_id=user.id, dep_iata=departure.iata, arr_iata=arrival.iata
            )
            .all()
        )
        data_in_table = tuple(
            (
                number,
                i.dep_time,
                i.dep_estimated,
                i.flight_iata,
                airline_names_list.get(i.airline_icao, "No Data"),
                i.dep_gate,
                i.dep_terminal,
                i.arr_gate,
                i.arr_terminal,
                i.arr_baggage,
                i.arr_time,
                i.arr_estimated,
                i.delayed,
                i.duration,
                i.status,
            )
            for number, i in enumerate(database_data_by_user, start=1)
        )

    return render_template(
        "flights.html",
        data_in_table=data_in_table,
        destination=destination_tuple,
        headings=headings,
        no_data=no_data,
    )


@main.route("/followed", methods=["POST", "GET"])
@login_required
def followed_flights():
    return render_template("followed.html")


# background process happening without any refreshing
@main.route("/background_process_test")
def background_process_test():

    return "nothing"
