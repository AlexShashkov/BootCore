from sqlalchemy import Column, Integer, ForeignKey

from source.database import Base
from source.database.models.user import User
from ._base_model import BaseServiceModel


class VK(Base, BaseServiceModel):
    __tablename__ = 'vks'

    external_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    vk_id = Column(Integer, unique=True)

    def __init__(self, external_id: int, vk_id: int):
        super().__init__(external_id=external_id)
        self.vk_id = int(vk_id)
