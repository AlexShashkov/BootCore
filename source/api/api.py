import functools

from flask import request, abort

from core import api_conf
from . import app
from .utils import *
from ..database.methods import Methods


def protected(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('XXX-CODE') == api_conf['secret_code']:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/bootcore/', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/bootcore/get_points', methods=['GET'])
def on_get_points():
    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id'), **request.args):
        return Reply.bad_request(error='Empty important args passed')

    methods = Methods(**request.args)
    if methods.user:
        return Reply.ok(points=methods.user.points)
    else:
        return Reply.bad_request(error='Invalid user\'s id passed')


@app.route('/bootcore/update_points', methods=['PUT'])
def on_add_points():
    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id'),
                                    **request.json) or not not check_args_important('count', **request.json):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods(**request.json)
    if methods.user:
        methods.update_points(request.json['count'])
        return Reply.ok()
    else:
        return Reply.bad_request(error='Invalid user\'s id passed')
