from sqlalchemy import Column, Integer, ForeignKey

from source.database import Base
from source.database.models.user import User
from .base_model import BaseServiceModel


class Discord(Base, BaseServiceModel):
    __tablename__ = 'discords'

    external_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    discord_id = Column(Integer, unique=True)

    def __init__(self, external_id: int, discord_id: int):
        super().__init__(external_id=external_id)
        self.discord_id = int(discord_id)
