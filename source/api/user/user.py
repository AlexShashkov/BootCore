from source.api import app
from source.database.models import *
from source.mail import *
from source.api.wraps import *
from source.database.models.service.utils import *
from ..utils import *


@app.route('/api/', methods=['GET'])
def on_root():
    return Reply.ok()


@app.route('/api/user/invoke_email', methods=['POST'])
@protected
def on_invoke_email():
    data = request.json

    if not check_args_important(('email',), **data):
        return Reply.bad_request(error='Empty important keys passed')

    code = None
    methods = Methods()
    _user = methods.get_user(email=data['email'])

    if _user:
        if _user.status == 'active':
            return Reply.conflict(error='User already activated')

    if methods.is_email_exists(data['email']) and not data.get('resend'):
        return Reply.bad_request(error='Email already exists')
    elif data.get('resend'):
        user = methods.get_user(email=data['email'])
        if not user or not user.note:
            return Reply.bad_request(error='Invalid user')
        code = user.note
    elif not methods.user or methods.user.status == 'inactive':
        code = generate_verification_code()
        user = User(email=data['email'], note=code)
        methods.add_user(user)

    Mail.send_confirmation(to=data['email'], code=code)
    return Reply.ok()


@app.route('/api/user/accept_email', methods=['POST'])  # May be put but post
@protected
def on_accept_email():
    data = request.json

    if not check_args_important(('code', 'email'), **data):
        return Reply.bad_request(error='Empty important keys passed')

    methods = Methods()
    user = methods.get_user(email=data['email'])
    if user and user.status == 'inactive':
        if user.note == data['code']:
            user.note = ''
            user.status = 'active'
            methods.update_user(user)
            return Reply.ok(user_id=user.id)
        else:
            return Reply.bad_request(error='Invalid code')
    else:
        return Reply.bad_request(error='Invalid email')


@app.route('/api/user/get', methods=['GET'])
@protected
@user_required
def on_get_user(**kwargs):
    if not kwargs.get(''):
        return Reply.bad_request(error='Empty or invalid locators passed')

    methods = Methods(user=kwargs.get(''))

    _user = methods.user.get_dict()

    for _s in get_services():
        if methods.user.__getattribute__(_s.lower()):
            _user.update(methods.user.__getattribute__(_s.lower()).get_dict())

    _user.pop('external_id', None)

    return Reply.ok(**_user)
