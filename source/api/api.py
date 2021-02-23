import functools
from flask import request, abort

from core import api_conf
from . import app
from .utils import *
from ..database.methods import Methods
from ..database.models import *
from ..mail import Mail
from ..utils import *
from ..database.exceptions import *


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
        return f(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/set_points', methods=['PUT'])
@protected
def on_set_points():
    data = request.json

    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id', 'id'),
                                    **data) or not check_args_important(('value',), **data):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods(**data)
    if methods.user:
        service = [x.replace('_id', '') for x in list(data) if x in ['twitch_id', 'vk_id', 'discord_id']]
        try:
            methods.set_points(request.json['value'], service=service[0] if service else None)
        except NotActive:
            return Reply.failed_dependency(error='User is not active')
        return Reply.ok()
    else:
        return Reply.bad_request(error='Invalid user id passed')


@app.route('/increase_points', methods=['PUT'])
@protected
def on_increase_points():
    data = request.json

    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id', 'id'),
                                    **data) or not check_args_important(('value',), **data):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods(**data)
    if methods.user:
        service = [x.replace('_id', '') for x in list(data) if x in ['twitch_id', 'vk_id', 'discord_id']]
        try:
            methods.increase_points(request.json['value'], service=service[0] if service else None)
        except NotActive:
            return Reply.failed_dependency(error='User is not active')
        return Reply.ok()
    else:
        return Reply.bad_request(error='Invalid user id passed')


@app.route('/decrease_points', methods=['PUT'])
@protected
def on_decrease_points():
    data = request.json

    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id', 'id'),
                                    **data) or not check_args_important(('value',), **data):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods(**data)
    if methods.user:
        service = [x.replace('_id', '') for x in list(data) if x in ['twitch_id', 'vk_id', 'discord_id']]
        try:
            methods.decrease_points(request.json['value'], service=service[0] if service else None)
        except NotActive:
            return Reply.failed_dependency(error='User is not active')
        return Reply.ok()
    else:
        return Reply.bad_request(error='Invalid user id passed')


@app.route('/invoke_email', methods=['POST'])
@protected
def on_invoke_email():
    data = request.json

    if not check_args_important(('email',), **data):
        return Reply.bad_request(error='Empty important keys passed')

    code = None
    methods = Methods()
    _user = methods.get_user_by_email(data['email'])

    if _user:
        if _user.status == 'active':
            return Reply.conflict(error='User already activated')

    if methods.is_email_exists(data['email']) and not data.get('resend'):
        return Reply.bad_request(error='Email already exists')
    elif data.get('resend'):
        user = methods.get_user_by_email(data['email'])
        if not user or not user.note:
            return Reply.bad_request(error='Invalid user')
        code = user.note
    elif not methods.user or methods.user.status == 'inactive':
        code = generate_verification_code()
        user = User(email=data['email'], note=code)
        methods.add_user(user)

    Mail.send_confirmation(to=data['email'], code=code)
    return Reply.ok()


@app.route('/accept_email', methods=['POST'])  # May be put but post
@protected
def on_accept_email():
    data = request.json

    if not check_args_important(('code', 'email'), **data):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods()
    user = methods.get_user_by_email(data['email'])
    if user and user.status == 'inactive':
        if user.note == data['code']:
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
def on_integrate():
    data = request.json

    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id'),
                                    **data) or not check_args_important(('email',), **data):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods()
    user = methods.get_user_by_email(data['email'])
    if not user:
        return Reply.bad_request(error='Invalid email')

    methods.user = user  # kinda bad way

    try:
        if data.get('twitch_id'):
            if user.twitch:
                return Reply.bad_request(error='Already integrated')
            methods.integrate_service(service.Twitch(user.id, data['twitch_id']))

        if data.get('vk_id'):
            if user.vk:
                return Reply.bad_request(error='Already integrated')
            try:
                int(data['vk_id'])
            except ValueError:
                return Reply.bad_request(error='Invalid vk_id')
            methods.integrate_service(service.VK(user.id, data['vk_id']))

        if data.get('discord_id'):
            if user.discord:
                return Reply.bad_request(error='Already integrated')
            methods.integrate_service(service.Discord(user.id, data['discord_id']))
    except NotActive:
        return Reply.failed_dependency(error='User is not active')

    return Reply.ok()


@app.route('/disintegrate', methods=['POST'])
@protected
def on_disintegrate():
    data = request.json

    if not check_args_non_important(('twitch', 'vk', 'discord'),
                                    **data) or not check_args_important(('email',), **data):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods()
    user = methods.get_user_by_email(data['email'])
    if not user:
        return Reply.bad_request(error='Invalid email')

    methods.user = user  # kinda bad way

    try:
        if data.get('twitch'):
            if not user.twitch:
                return Reply.bad_request(error='Service does not exists')
            methods.disintegrate_service(user.twitch)

        if data.get('vk'):
            if not user.vk:
                return Reply.bad_request(error='Service does not exists')
            methods.disintegrate_service(user.vk)

        if data.get('discord'):
            if not user.discord:
                return Reply.bad_request(error='Service does not exists')
            methods.disintegrate_service(user.discord)
    except NotActive:
        return Reply.failed_dependency(error='User is not active')

    return Reply.ok()


@app.route('/get_user', methods=['GET'])
@protected
def on_get_user():
    data = request.json

    if not check_args_non_important(('twitch_id', 'vk_id', 'discord_id', 'id'), **data):
        return Reply.bad_request(error='Empty important args passed')

    methods = Methods(**data)
    if methods.user:
        _user = methods.user.get_dict()

        # TODO: Refactor
        if methods.user.vk:
            _user.update(methods.user.vk.get_dict())

        if methods.user.discord:
            _user.update(methods.user.twitch.get_dict())

        if methods.user.twitch:
            _user.update(methods.user.discord.get_dict())

        _user.pop('external_id', None)

        return Reply.ok(**_user)
    else:
        return Reply.bad_request(error='Invalid user id passed')
