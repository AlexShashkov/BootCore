from .models.service._base_model import BaseServiceModel


def is_service_object(s_object: object) -> bool:
    return isinstance(s_object, BaseServiceModel)
