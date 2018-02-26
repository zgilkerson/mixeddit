import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')
client_id = config['spotify']['client_id']
client_secret = config['spotify']['client_secret']
scopes = 'user-read-private playlist-read-private playlist-modify-private'
redirect_uri='http://localhost:666' # DOOM! should switch this over once a front-end is made...if ever
response_type='code'