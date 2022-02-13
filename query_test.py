from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:MarJak12!@172.19.112.1/airports'  # SQL personal key, for testing purpose I will leave it
app.config['SECRET_KEY'] = 'MY SECERT KEY LOL 1969!'  # FLASK personal key, for testing purpose I will leave it


db = SQLAlchemy(app)


class AIRLABS_Airlines(db.Model):  # SQLalchemy model
    __tablename__ = 'airlines_database'
    index = db.Column(db.String(50), unique=False, nullable=False, primary_key=True)
    icao_code = db.Column(db.String(50), unique=False, nullable=False, primary_key=True)
    iata_code = db.Column(db.String(50), unique=False, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)

    def as_self(self):
        return self.name


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        database_data = AIRLABS_Airlines.query.all()
        airlines = [i.as_self() for i in database_data]
        return render_template("index.html",
                               airlines=airlines)


if __name__ == '__main__':
    app.run(debug=True)
