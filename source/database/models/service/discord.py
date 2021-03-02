from sqlalchemy import Column, Integer, ForeignKey, String

from source.database import Base
from source.database.models.user import User
from ._base_model import BaseServiceModel


class Discord(Base, BaseServiceModel):
    __tablename__ = 'discords'

    external_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    discord_id = Column(String, unique=True)  # May be int, but don't know

    def __init__(self, external_id: int, discord_id: str):
        super().__init__(external_id=external_id)
        self.discord_id = discord_id
