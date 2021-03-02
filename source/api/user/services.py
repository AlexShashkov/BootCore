from source.api import app
from source.api.wraps import *
from source.database.exceptions import *
from source.database.models.service.utils import *
from ..utils import *


@app.route('/api/user/services/integrate', methods=['POST'])
@protected
def on_integrate():
    data = request.json

    if not check_args_important(('email', 'services'), **data):
        return Reply.bad_request(error='Empty important keys passed')

    if not isinstance(data['services'], dict):
        return Reply.bad_request(error='Invalid services type')

    if not all([is_str_service(x) for x in data['services']]):
        return Reply.bad_request(error='Invalid services passed')

    methods = Methods()
    user = methods.get_user(email=data['email'])
    if not user:
        return Reply.bad_request(error='Invalid email')

    methods.user = user

    for _s in data['services']:
        if is_str_service(_s):
            if user.__getattribute__(_s):
                return Reply.bad_request(error=f'Service {_s} already integrated')
            try:
                methods.integrate_service(get_service_from_str(_s)(user.id, data['services'][_s]))
            except NotActive:
                return Reply.failed_dependency(error='User is not active')
        else:
            return Reply.bad_request(error=f'Service {_s} is not a valid service')

    return Reply.ok()


@app.route('/api/user/services/disintegrate', methods=['POST'])
@protected
def on_disintegrate():
    data = request.json

    if not check_args_important(('email', 'services'), **data):
        return Reply.bad_request(error='Empty important keys passed')

    if not isinstance(data['services'], dict):
        return Reply.bad_request(error='Invalid services type')

    if not all([is_str_service(x) for x in data['services']]):
        return Reply.bad_request(error='Invalid services passed')

    methods = Methods()
    user = methods.get_user(email=data['email'])
    if not user:
        return Reply.bad_request(error='Invalid email')

    methods.user = user

    for _s in data['services']:
        if is_str_service(_s):
            if not user.__getattribute__(_s):
                return Reply.bad_request(error=f'Service {_s} not integrated yet')
            try:
                methods.disintegrate_service(user.__getattribute__(_s))
            except NotActive:
                return Reply.failed_dependency(error='User is not active')
        else:
            return Reply.bad_request(error=f'Service {_s} is not a valid service')

    return Reply.ok()
