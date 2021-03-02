from flask import Flask
from core import api_conf

app = Flask(__name__)
app.config['SECRET_KEY'] = api_conf['secret_key']

__all__ = ['app']

from .user import *
