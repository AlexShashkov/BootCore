from flask import Flask

from core import api_conf

app = Flask(__name__)
app.config['SECRET_KEY'] = api_conf['secret_key']
app.config['APPLICATION_ROOT'] = '/bootcore/'  # Seems doesn't work

__all__ = ['app']

from .api import *
