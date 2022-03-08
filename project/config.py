import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

DATABASE_URL = os.environ["CONNECTION_LINK"]
FLASK_KEY = os.environ["FLASK_KEY"]

AIRLABS_API_KEY = os.environ["AIRLABS_API_KEY"]
API_BASE = "http://airlabs.co/api/v9/"

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
DEFAULT_EMAIL = "apptesting.mj@gmail.com"
FROM_EMAIL = os.environ.get("FROM_EMAIL", DEFAULT_EMAIL)
FERNET_KEY = os.environ.get("FERNET_KEY")
