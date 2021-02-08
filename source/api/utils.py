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

    @staticmethod
    def conflict(**kwargs) -> tuple:
        if not kwargs:
            kwargs = {'status': False, 'error': 'Conflict'}
        kwargs['status'] = False
        return json.dumps(kwargs), 409

    @staticmethod
    def not_found(**kwargs) -> tuple:
        if not kwargs:
            kwargs = {'status': False, 'error': 'Not found'}
        kwargs['status'] = False
        return json.dumps(kwargs), 404

    @staticmethod
    def unknown_error(**kwargs) -> tuple:
        if not kwargs:
            kwargs = {'status': False, 'error': 'Something went wrong...'}
        kwargs['status'] = False
        return json.dumps(kwargs), 520
