import json


class BaseModel:
    def json(self) -> str:
        return json.dumps(vars(self), ensure_ascii=False)
