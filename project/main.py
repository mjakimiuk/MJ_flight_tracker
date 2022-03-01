from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from .app_backend import airlabs_schedules_data_into_sql
from .models import Airlines_database, Airport_database, Airport_Schedules_database
from .sendgrid_app import send_email_sendgrid

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

    database_data = Airport_database.query.all()
    airports = [i.name_city for i in database_data]
    return render_template("index.html", name=current_user.name, airports=airports)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@main.route("/flights", methods=["POST", "GET"])
@login_required
def flights():
    departure = Airport_database.query.filter(
        Airport_database.name_city == request.form.get("airport_1")
    ).first()
    arrival = Airport_database.query.filter(
        Airport_database.name_city == request.form.get("airport_2")
    ).first()
    no_data = ""
    if airlabs_schedules_data_into_sql(departure.iata, arrival.iata) is False:
        no_data = "No Data"
        data_in_table = "No Data"
        destination_tuple = "No Data"
    else:
        airlabs_schedules_data_into_sql(departure.iata, arrival.iata)
        database_data = Airport_Schedules_database.query.all()
        airline_names_codes = [i.airline_icao for i in database_data]
        airline_names = Airlines_database.query.filter(
            Airlines_database.icao_code.in_(airline_names_codes)
        )
        airline_names_list = {i.icao_code: i.name for i in airline_names}
        destination_tuple = (
            request.form.get("airport_1"),
            request.form.get("airport_2"),
        )
        data_in_table = tuple(
            (
                i.index,
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
            for i in database_data
        )

    return render_template(
        "flights.html",
        data_in_table=data_in_table,
        destination=destination_tuple,
        headings=headings,
        no_data=no_data,
    )


# background process happening without any refreshing
@main.route("/background_process_test")
def background_process_test():
    recipient = "marcin.jakimiuk@gmail.com"
    send_email_sendgrid(recipient)
    return "nothing"
