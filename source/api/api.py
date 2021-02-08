import functools
# from ..mail import Mail
from datetime import datetime

from flask import request, abort
from pytz import timezone

from core import api_conf
from . import app
from .utils import *
from ..database.methods import Methods
from ..database.models import *
from ..utils import *


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
        if not request.headers.get('XXX-CODE') == api_conf['secret_code']:
            abort(403)
        elif not request.args and not request.json:
            abort(400)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/set_points', methods=['PUT'])
@protected
@important_input
def on_set_points():
    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id'),
                                    **request.json) or not check_args_important(('value',), **request.json):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods(**request.json)
    if methods.user:
        methods.set_points(request.json['value'])
        return Reply.ok()
    else:
        return Reply.bad_request(error='Invalid user id passed')


@app.route('/increase_points', methods=['PUT'])
@protected
@important_input
def on_increase_points():
    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id'),
                                    **request.json) or not check_args_important(('value',), **request.json):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods(**request.json)
    if methods.user:
        methods.increase_points(request.json['value'])
        return Reply.ok()
    else:
        return Reply.bad_request(error='Invalid user id passed')


@app.route('/decrease_points', methods=['PUT'])
@protected
@important_input
def on_decrease_points():
    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id'),
                                    **request.json) or not check_args_important(('value',), **request.json):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods(**request.json)
    if methods.user:
        methods.decrease_points(request.json['value'])
        return Reply.ok()
    else:
        return Reply.bad_request(error='Invalid user id passed')


@app.route('/invoke_email', methods=['POST'])
@protected
@important_input
def on_invoke_email():
    if not check_args_important(('email',), **request.json):
        return Reply.bad_request(error='Empty important keys passed')

    code = None
    methods = Methods()
    if methods.is_email_exists(request.json['email']) and not request.json.get('resend'):
        return Reply.bad_request(error='Email already exists')
    elif request.json.get('resend'):
        user = methods.get_user_by_email(request.json['email'])
        if not user or not user.note:
            return Reply.bad_request(error='Invalid user')
        code = user.note
    elif not methods.user or methods.user.status == 'inactive':
        code = generate_verification_code()
        user = User(email=request.json['email'], registered_ts=int(datetime.now(timezone('Europe/Moscow')).timestamp()),
                    note=code)
        methods.add_user(user)
    else:
        return Reply.conflict(error='User already activated')

    # mail_result = Mail.send_confirmation(request.json['email'], code)
    # if mail_result[0] != 200:
    #     return Reply.unknown_error(error=str(mail_result[1]))
    return Reply.ok(code=code)  # Only for tests


@app.route('/accept_email', methods=['PUT'])
@protected
@important_input
def on_accept_email():
    if not check_args_important(('code', 'email'), **request.json):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods()
    user = methods.get_user_by_email(request.json['email'])
    if user and user.status == 'inactive':
        if user.note == request.json['code']:
            user.note = ''
            user.status = 'active'
            methods.update_user(user)
            return Reply.ok()
        else:
            return Reply.bad_request(error='Invalid code')
    else:
        return Reply.bad_request(error='Invalid email')


@app.route('/integrate', methods=['POST'])
@protected
@important_input
def on_integrate():
    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id'),
                                    **request.json) or not check_args_important(('email',), **request.json):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods()
    user = methods.get_user_by_email(request.json['email'])
    if not user:
        return Reply.bad_request(error='Invalid email')

    methods.user = user  # kinda bad way

    if request.json.get('twitch_id'):
        methods.integrate_service(service.Twitch(user.id, request.json['twitch_id']))

    if request.json.get('vk_id'):
        methods.integrate_service(service.VK(user.id, request.json['vk_id']))

    if request.json.get('discord_id'):
        methods.integrate_service(service.VK(user.id, request.json['discord_id']))

    return Reply.ok()


@app.route('/get_user', methods=['GET'])
@protected
@important_input
def on_get_user():
    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id'), **request.args):
        return Reply.bad_request(error='Empty important args passed')

    methods = Methods(**request.args)
    if methods.user:
        return Reply.ok(**json.loads(methods.user.json()))  # ok good
    else:
        return Reply.bad_request(error='Invalid user id passed')
