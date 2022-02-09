import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()
# Import Data Models
from .redditor import Redditor
from .submission import Submission
from .indie_sunday import IndieSunday


def get_db_file():
    with open(os.path.join(os.getcwd(), "reddit_automation_suite/config.yaml")) as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
        return config["database"]


def get_engine():
    engine = create_engine(f"sqlite:///{get_db_file()}")
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine


engine = get_engine()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
