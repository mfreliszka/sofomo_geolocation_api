from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.settings import settings


Base = declarative_base()

engine = create_engine(settings.database_url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
