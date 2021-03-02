import hues
from requests import session

host = 'http://localhost:1337'
test_email = 'lol@kek.org'
test_vk = 333
test_discord = 'kek'
test_twitch = 'lol'
sess = session()
sess.headers = {'XXX-CODE': '##CODE##'}


def exec_error(method: str, response: str, status_code: int):
    hues.error(f'Method: {method}\nResponse: {response}\nStatus Code: {status_code}')
    exit(-1)


# Root
r = sess.get(host + '/api/')
if r.status_code == 200:
    hues.success('/api/')
else:
    exec_error('/api/', r.text, r.status_code)

# Invoke email
r = sess.post(host + '/api/user/invoke_email', json={
    'email': test_email
})
if r.status_code == 200:
    hues.success('/api/user/invoke_email')
else:
    exec_error('/api/user/invoke_email', r.text, r.status_code)

# Accept email
r = sess.post(host + '/api/user/accept_email', json={
    'email': test_email,
    'code': input('Code from email: ')
})
if r.status_code == 200:
    hues.success('/api/user/accept_email')
else:
    exec_error('/api/user/accept_email', r.text, r.status_code)

# Get user
r = sess.get(host + f'/api/user/get?email={test_email}')
if r.status_code == 200:
    hues.success(f'/api/user/get?email={test_email}')
else:
    exec_error(f'/api/user/get?email={test_email}', r.text, r.status_code)

# Integrate
r = sess.post(host + '/api/user/services/integrate', json={
    'services': {
        'vk': test_vk,
        'discord': test_discord,
        'twitch': test_twitch
    },
    'email': test_email
})
if r.status_code == 200:
    hues.success('/api/user/services/integrate')
else:
    exec_error('/api/user/services/integrate', r.text, r.status_code)

# Disintegrate
r = sess.post(host + '/api/user/services/disintegrate', json={
    'services': {
        'discord': True,
        'twitch': True
    },
    'email': test_email
})
if r.status_code == 200:
    hues.success('/api/user/services/disintegrate')
else:
    exec_error('/api/user/services/disintegrate', r.text, r.status_code)

# Set points
r = sess.put(host + '/api/user/economy/set_points', json={
    'vk': test_vk,
    'value': 300
})
if r.status_code == 200:
    hues.success('/api/user/economy/set_points')
else:
    exec_error('/api/user/economy/set_points', r.text, r.status_code)

# Increase points
r = sess.put(host + '/api/user/economy/increase_points', json={
    'vk': test_vk,
    'value': 150
})
if r.status_code == 200:
    hues.success('/api/user/economy/increase_points')
else:
    exec_error('/api/user/economy/increase_points', r.text, r.status_code)

# Decrease points
r = sess.put(host + '/api/user/economy/decrease_points', json={
    'vk': test_vk,
    'value': 600
})
if r.status_code == 200:
    hues.success('/api/user/economy/decrease_points')
else:
    exec_error('/api/user/economy/decrease_points', r.text, r.status_code)
