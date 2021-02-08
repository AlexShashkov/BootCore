from sqlalchemy import Column, Integer, String

from .base_model import BaseModel
from .. import Base


class User(Base, BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=True)
    points = Column(Integer, default=0)
    registered_ts = Column(Integer)
    status = Column(String, default='inactive')

    def __init__(self, registered_ts: int, status='inactive', email=None, points=0):
        self.points = points
        self.registered_ts = registered_ts
        self.points = points
        self.status = status
        self.email = email

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
