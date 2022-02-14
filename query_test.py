from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:MarJak12!@172.19.112.1/airports'  # SQL personal key, for testing purpose I will leave it
app.config['SECRET_KEY'] = 'MY SECERT KEY LOL 1969!'  # FLASK personal key, for testing purpose I will leave it


db = SQLAlchemy(app)


class Airport_database(db.Model):  # SQLalchemy model
    __tablename__ = 'airport_database_table'
    index = db.Column(db.String(100), unique=False, nullable=False, primary_key=True)
    iata = db.Column(db.String(100), unique=False, nullable=False, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False, primary_key=True)
    city = db.Column(db.String(100), unique=False, nullable=False)
    name_city = db.Column(db.String(100), unique=False, nullable=False)

    def as_self(self):
        return self.name_city


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        database_data = Airport_database.query.all()
        airlines = [i.as_self() for i in database_data]
        return render_template("index.html",
                               airlines=airlines)
    if request.method == "POST":
        flights()

@app.route("/flights", methods=["POST", "GET"])
def flights():
    return render_template("flights.html")


if __name__ == '__main__':
    app.run(debug=True)