from sqlalchemy import Column, Integer, ForeignKey, String

from source.database import Base
from source.database.models.user import User
from .base_model import BaseServiceModel


class Twitch(Base, BaseServiceModel):
    __tablename__ = 'twitches'

    external_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    twitch_id = Column(String, unique=True) # May be int, but don't know

    def __init__(self, external_id: int, twitch_id: int):
        super().__init__(external_id=external_id)
        self.twitch_id = twitch_id
