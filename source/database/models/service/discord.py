from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from source.database import Base
from source.database.models.user import User
from .base_model import BaseServiceModel


class Discord(Base, BaseServiceModel):
    __tablename__ = 'discords'

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    discord_id = Column(Integer, unique=True)
    user = relationship('User', backref='discord_id')

    def __init__(self, discord_id: int):
        self.discord_id = discord_id
