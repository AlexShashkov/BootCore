from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', echo=False)
Base = declarative_base()
from .models import *

Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)

__all__ = ['Session', 'engine']
