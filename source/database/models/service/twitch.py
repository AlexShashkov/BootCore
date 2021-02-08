from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from source.database import Base
from source.database.models.user import User
from .base_model import BaseServiceModel


class Twitch(Base, BaseServiceModel):
    __tablename__ = 'twitches'

    external_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    twitch_id = Column(Integer, unique=True)
    user = relationship('User', backref='twitch_id')

    def __init__(self, external_id: int, twitch_id: int):
        super().__init__(external_id=external_id)
        self.twitch_id = int(twitch_id)
