from . import Session
from .models import *


class Methods:
    def __init__(self, **kwargs):
        self.__session = Session()
        self.user = self.__get_user(**kwargs)

    def __get_user(self, **kwargs) -> User:
        result = None

        if not any(vars()):
            return None
        elif kwargs.get('vk_id'):
            result = [x for x in self.__session.query(service.VK).filter(service.VK.vk_id == kwargs['vk_id'])]
        elif kwargs.get('discord_id'):
            result = [x for x in
                      self.__session.query(service.Discord).filter(service.Discord.discord_id == kwargs['discord_id'])]
        elif kwargs.get('twitch_id'):
            result = [x for x in
                      self.__session.query(service.Twitch).filter(service.Twitch.twitch_id == kwargs['twitch_id'])]

        return result[0].user if result else None

    def update_points(self, count: int) -> None:
        self.user.points = count
        self.__session.commit()
