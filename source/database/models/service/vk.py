from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from source.database import Base
from source.database.models.user import User
from .base_model import BaseServiceModel


class VK(Base, BaseServiceModel):
    __tablename__ = 'vks'

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    vk_id = Column(Integer, unique=True)
    user = relationship('User', backref='vk_id')

    def __init__(self, vk_id: int):
        self.vk_id = vk_id
