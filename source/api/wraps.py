import functools
from flask import request, abort
from ..database.methods import Methods


def important_input(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.args and not request.json:
            abort(400)
        return f(*args, **kwargs)

    return decorated_function


def protected(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # if not request.headers.get('XXX-CODE') == api_conf['secret_code']:
        #     abort(403)
        return f(*args, **kwargs)

    return decorated_function


def user_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'GET':
            data = request.args
        else:
            data = request.json

        kwargs['user'] = Methods().get_user(**data)

        return f(*args, **kwargs)

    return decorated_function
