import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, User, Airport, Schedules, Airlines

load_dotenv()


def _create_session():
    db_url = os.environ['CONNECTION_LINK']
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    return create_session()


session = _create_session()
