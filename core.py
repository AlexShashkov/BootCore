import json

__version__ = '0.2.0'

config = json.load(open('config.json', 'r'))

api_conf = config['api']
mail_conf = config['mail']
db_conf = config['database']