from source.api import app
from source.api.wraps import *
from source.database.exceptions import *
from ..utils import *


@app.route('/api/user/economy/set_points', methods=['PUT'])
@protected
@user_required
def on_set_points(**kwargs):
    data = request.json

    if not data.get('value'):
        return Reply.bad_request(error='Empty value passed')

    if not kwargs.get('user'):
        return Reply.bad_request(error='Empty or invalid locators passed')

    methods = Methods(user=kwargs['user'])
    service = [x.replace('_id', '') for x in list(data) if x in ['twitch_id', 'vk_id', 'discord_id']]
    try:
        methods.set_points(int(request.json['value']), service=service[0] if service else None)
    except NotActive:
        return Reply.failed_dependency(error='User is not active')
    except ValueError:
        return Reply.bad_request(error='Invalid value')
    return Reply.ok(points=methods.user.points)


@app.route('/api/user/economy/increase_points', methods=['PUT'])
@protected
@user_required
def on_increase_points(**kwargs):
    data = request.json

    if not data.get('value'):
        return Reply.bad_request(error='Empty value passed')

    if not kwargs.get('user'):
        return Reply.bad_request(error='Empty or invalid locators passed')

    methods = Methods(user=kwargs['user'])

    service = [x.replace('_id', '') for x in list(data) if x in ['twitch_id', 'vk_id', 'discord_id']]
    try:
        methods.increase_points(int(request.json['value']), service=service[0] if service else None)
    except NotActive:
        return Reply.failed_dependency(error='User is not active')
    except ValueError:
        return Reply.bad_request(error='Invalid value')
    return Reply.ok(points=methods.user.points)


@app.route('/api/user/economy/decrease_points', methods=['PUT'])
@protected
@user_required
def on_decrease_points(**kwargs):
    data = request.json

    if not data.get('value'):
        return Reply.bad_request(error='Empty value passed')

    if not kwargs.get('user'):
        return Reply.bad_request(error='Empty or invalid locators passed')

    methods = Methods(user=kwargs['user'])

    service = [x.replace('_id', '') for x in list(data) if x in ['twitch_id', 'vk_id', 'discord_id']]
    try:
        methods.decrease_points(int(request.json['value']), service=service[0] if service else None)
    except NotActive:
        return Reply.failed_dependency(error='User is not active')
    except ValueError:
        return Reply.bad_request(error='Invalid value')
    return Reply.ok(points=methods.user.points)