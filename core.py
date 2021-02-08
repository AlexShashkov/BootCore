import json

__version__ = '0.0.1'

config = json.load(open('config.json', 'r'))
api_conf = config['api']
