from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core import db_conf

engine = create_engine('postgresql+psycopg2://{user}:{password}//:@{host}:{port}/{db}'.format(
    user=db_conf['user'],
    password=db_conf['password'],
    db=db_conf['db'],
    host=db_conf['host'],
    port=db_conf['port']
), echo=False)

Base = declarative_base()
from .models import *

Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)

__all__ = ['Session', 'engine']
