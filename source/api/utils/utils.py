import json


def check_args_important(_args, **kwargs):
    for x in _args:
        if x not in kwargs.keys() or not kwargs.get(x):
            return False
    return True


def check_args_non_important(_args, **kwargs):
    for x in _args:
        if kwargs.get(x):
            return True
    return False


class Reply:
    @staticmethod
    def ok(**kwargs) -> tuple:
        if not kwargs:
            kwargs = {'status': True, 'message': 'OK'}
        kwargs['status'] = True
        return json.dumps(kwargs), 200

    @staticmethod
    def bad_request(**kwargs) -> tuple:
        if not kwargs:
            kwargs = {'status': False, 'error': 'Bad request'}
        kwargs['status'] = False
        return json.dumps(kwargs), 400

    @staticmethod
    def forbidden(**kwargs) -> tuple:
        if not kwargs:
            kwargs = {'status': False, 'error': 'Forbidden'}
        kwargs['status'] = False
        return json.dumps(kwargs), 403
