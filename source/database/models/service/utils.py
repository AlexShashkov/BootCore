from importlib import import_module


def is_str_service(_service: str) -> bool:
    try:
        if _service.startswith('_'):
            raise ImportError
        import_module(f'.{_service}', 'source.database.models.service')
        return True
    except ImportError as e:
        print(str(e))
        return False


def get_service_from_str(_service: str):
    if not is_str_service(_service):
        return None

    # Really cool, but..............
    # TODO: Refactor

    _module = import_module(f'.{_service}', 'source.database.models.service')
    for _s in dir(_module):
        if _s.lower() == _service.lower():
            return _module.__getattribute__(_s)
    return None


def get_services() -> tuple:
    _module = import_module(f'.service', 'source.database.models')
    return tuple(_module.__getattribute__('__all__'))
