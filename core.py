import json

__version__ = '0.1.2'

config = json.load(open('config.json', 'r'))
api_conf = config['api']
mail_conf = config['mail']
