from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import Airport_database, Airport_Schedules_database
from .app_backend import airlabs_schedules_data_into_sql

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    
    database_data = Airport_database.query.all()
    airlines = [i.name_city for i in database_data]
    return render_template('index.html', name=current_user.name, airlines=airlines)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route("/flights", methods=["POST", "GET"])
@login_required
def flights():
    departure = Airport_database.query.filter(Airport_database.name_city == request.form.get('airport_1')).first()
    arrival = Airport_database.query.filter(Airport_database.name_city == request.form.get('airport_2')).first()
    airlabs_schedules_data_into_sql(departure.iata,arrival.iata)
    database_data = Airport_Schedules_database.query.all()
    if not database_data:
        database_data = ''

    
    return render_template("flights.html",
                            database_data=database_data)