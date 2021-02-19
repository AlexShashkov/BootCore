import unittest

import requests

headers = {'XXX-CODE': '123'}
session = requests.Session()
session.headers = headers
code = None


class TestStringMethods(unittest.TestCase):
    def test_root(self):
        context = session.get('http://localhost:5000/')
        self.assertEqual(context.status_code, 200)

    def test_mail(self):
        context = session.post('http://localhost:5000/invoke_email', json={'email': 'test_eeemail@mail.ru'})
        code = context.json().get('response', {}).get('code')
        self.assertEqual(context.status_code, 200)
        context = session.put('http://localhost:5000/accept_email',
                              json={'email': 'test_eeemail@mail.ru', 'code': code})
        self.assertEqual(context.status_code, 200)

    def test_integrate_vk(self):
        context = session.post('http://localhost:5000/integrate',
                               json={'email': 'test_eeemail@mail.ru', 'vk_id': 1233})
        self.assertEqual(context.status_code, 200)

    def test_get_user(self):
        context = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(context.get('response', {}).get('email'), 'test_eeemail@mail.ru')

    def test_increase_points(self):
        session.put('http://localhost:5000/set_points',
                    json={'vk_id': '1233', 'value': 0})
        user = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(user.get('response', {}).get('points'), 0)
        context = session.put('http://localhost:5000/increase_points',
                              json={'vk_id': '1233', 'value': 600})
        user = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(user.get('response', {}).get('points'), 600)
        context = session.put('http://localhost:5000/increase_points',
                              json={'vk_id': '1233', 'value': -600})
        user = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(user.get('response', {}).get('points'), 1200)
        context = session.put('http://localhost:5000/increase_points',
                              json={'vk_id': '1233', 'value': -0})
        user = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(user.get('response', {}).get('points'), 1200)

    def test_decrease_points(self):
        session.put('http://localhost:5000/set_points',
                    json={'vk_id': '1233', 'value': 0})
        user = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(user.get('response', {}).get('points'), 0)
        context = session.put('http://localhost:5000/decrease_points',
                              json={'vk_id': '1233', 'value': -800})
        user = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(user.get('response', {}).get('points'), 0)
        context = session.put('http://localhost:5000/decrease_points',
                              json={'vk_id': '1233', 'value': -0})
        user = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(user.get('response', {}).get('points'), 0)

    def test_set_points(self):
        context = session.put('http://localhost:5000/set_points',
                              json={'vk_id': '1233', 'value': 9999999999999999999999999999999999999})
        user = session.get('http://localhost:5000/get_user?vk_id=1233').json()
        self.assertEqual(user.get('response', {}).get('points'), 2 ** 30)


if __name__ == '__main__':
    unittest.main()
