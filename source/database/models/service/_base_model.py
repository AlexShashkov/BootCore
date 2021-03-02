from ..base_model import BaseModel


class BaseServiceModel(BaseModel):
    def __init__(self, external_id: int):
        self.external_id = external_id

    def __repr__(self):
        return f"<Service={self.__class__.__name__}>"
