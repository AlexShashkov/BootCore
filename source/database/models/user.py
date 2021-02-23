from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from .. import Base
from datetime import datetime
from pytz import timezone


class User(Base, BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=True)
    points = Column(BigInteger, default=0)
    registered_ts = Column(BigInteger, nullable=False)
    status = Column(String, nullable=False, default='inactive')
    note = Column(String, nullable=True)

    vk = relationship('VK', backref='vk', uselist=False)
    discord = relationship('Discord', backref='discord', uselist=False)
    twitch = relationship('Twitch', backref='twitch', uselist=False)

    def __init__(self, status='inactive', email=None, points=0, note=None, registered_ts=int(datetime.now(timezone('Europe/Moscow')).timestamp())):
        self.points = points
        self.registered_ts = registered_ts
        self.status = status
        self.email = email
        self.note = note

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
