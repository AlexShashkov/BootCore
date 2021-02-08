from sqlalchemy import Column, Integer, String, ForeignKey

from .base_model import BaseModel
from .user import User
from .. import Base


class PointsHistory(Base, BaseModel):
    __tablename__ = 'points_history'

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    service = Column(String)
    count = Column(Integer)
    ts = Column(Integer)

    def __init__(self, user_id: int, service: str, count: int, ts: int):
        self.user_id = user_id
        self.service = service
        self.count = count
        self.ts = ts

    def __repr__(self):
        return f"<PointsHistory(user_id={self.user_id}, count={self.count})>"
