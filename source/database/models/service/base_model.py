from ..base_model import BaseModel


class BaseServiceModel(BaseModel):
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.user_id}, {self.__class__.__name__.lower()}_id={getattr(self, self.__class__.__name__.lower())})>"
