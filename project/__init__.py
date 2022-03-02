import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


def create_app():
    app = Flask(__name__)

    # TODO: could move dotenv and all config variable parsing to one config.py
    # module
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["CONNECTION_LINK"]
    app.config["SECRET_KEY"] = os.environ["FLASK_KEY"]

    db = SQLAlchemy()
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
