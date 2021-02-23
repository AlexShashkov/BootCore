from sqlalchemy import Column, Integer, String, ForeignKey

from .base_model import BaseModel
from .user import User
from .. import Base
from datetime import datetime
from pytz import timezone


class Transaction(Base, BaseModel):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    service = Column(String)
    delta = Column(Integer)
    ts = Column(Integer)

    def __init__(self, user_id: int, service: str, delta: int, ts=int(datetime.now(timezone('Europe/Moscow')).timestamp())):
        self.user_id = user_id
        self.service = service
        self.delta = delta
        self.ts = ts

    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, delta={self.delta})>"
