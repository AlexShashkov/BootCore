from copy import copy


class BaseModel:
    def get_dict(self) -> dict:
        _vars = copy(vars(self))
        _vars.pop('_sa_instance_state')
        # for var in list(_vars):
        #     if issubclass(_vars[var].__class__, BaseModel):
        #         _vars[var] = _vars[var].get_dict()
        # TODO: Refactor
        _vars.pop('vk', None)
        _vars.pop('discord', None)
        _vars.pop('twitch', None)

        return _vars
