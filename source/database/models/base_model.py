import json


class BaseModel:
    def json(self) -> str:
        _vars = vars(self)
        _vars.pop('_sa_instance_state')
        return json.dumps(_vars, ensure_ascii=False)
