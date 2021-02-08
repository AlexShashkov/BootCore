from sqlalchemy import Column, String, BigInteger, Integer

from .base_model import BaseModel
from .. import Base


class User(Base, BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=True)
    points = Column(BigInteger, default=0)
    registered_ts = Column(BigInteger, nullable=False)
    status = Column(String, nullable=False, default='inactive')
    note = Column(String, nullable=True)

    def __init__(self, registered_ts: int, status='inactive', email=None, points=0, note=None):
        self.points = points
        self.registered_ts = registered_ts
        self.status = status
        self.email = email
        self.note = note

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
