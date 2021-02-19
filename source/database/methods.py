from . import Session
from .models import *
from .utils import *


class Methods:
    def __init__(self, **kwargs):
        self.__session = Session()
        self.user = self.get_user_by_id(**kwargs) if kwargs else None

    def add_user(self, user: User) -> None:
        self.__session.add(user)
        self.__session.commit()

    def is_email_exists(self, email: str) -> bool:
        return bool([x for x in self.__session.query(User).filter(User.email == email)])

    def is_service_exists(self, s_object: object) -> bool:
        if not is_service_object(s_object):
            raise TypeError('Not a service object')
        return bool([x for x in self.__session.query(s_object.__class__).filter(
            s_object.__class__.external_id == s_object.external_id)])

    def update_user(self, user: User) -> None:
        self.user = user
        self.__session.commit()

    def remove_user(self, user: User) -> None:
        self.__session.delete(user)
        self.__session.commit()

    def get_user_by_id(self, **kwargs) -> User:
        result = None

        if kwargs.get('vk_id'):
            result = [x for x in self.__session.query(service.VK).filter(service.VK.vk_id == kwargs['vk_id'])]
        elif kwargs.get('discord_id'):
            result = [x for x in
                      self.__session.query(service.Discord).filter(service.Discord.discord_id == kwargs['discord_id'])]
        elif kwargs.get('twitch_id'):
            result = [x for x in
                      self.__session.query(service.Twitch).filter(service.Twitch.twitch_id == kwargs['twitch_id'])]
        elif kwargs.get('id'):
            result = [x for x in self.__session.query(User).filter(User.id == kwargs.get('id'))]

        if result:
            if issubclass(result[0].__class__, BaseServiceModel):
                return self.get_user_by_id(id=result[0].external_id)
            else:
                return result[0]

    def get_user_by_email(self, email: str) -> User:
        result = [x for x in self.__session.query(User).filter(User.email == email)]
        return result[0] if result else None

    def set_points(self, value: int) -> None:
        if value > 2 ** 30:
            value = 2 ** 30
        elif value < 0:
            value = 0
        self.user.points = value
        self.__session.commit()

    def increase_points(self, value: int) -> None:
        value = abs(value)
        if self.user.points + value > 2 ** 30:
            self.user.points = 2 ** 30
        else:
            self.user.points += value
        self.__session.commit()

    def decrease_points(self, value: int) -> None:
        value = abs(value)
        if self.user.points - value < 0:
            self.user.points = 0
        else:
            self.user.points -= value
        self.__session.commit()

    def integrate_service(self, s_object: object) -> None:
        if not is_service_object(s_object):
            raise TypeError('Not a service object')
        self.__session.add(s_object)
        self.__session.commit()
