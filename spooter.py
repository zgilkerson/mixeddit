import configparser
import json
import requests
from requests_oauthlib import OAuth2Session

# class spooter:
config = configparser.ConfigParser()
configFile = 'config.ini'
config.read(configFile)
client_id = config['spotify']['client_id']
client_secret = config['spotify']['client_secret']
token = json.loads(config['spotify']['token'])
scope = 'user-read-private playlist-read-private playlist-modify-private'
redirect_uri='https://localhost:666' # DOOM! should switch this over once a front-end is made...if ever
response_type='code'
spotifyUrlAuthBase = 'https://accounts.spotify.com/api/'

extra = {
    'client_id': client_id,
    'client_secret': client_secret,
}

def save_token(newToken):
    config['spotify']['token'] = json.dumps(newToken)
    # token = newToken
    with open(configFile, 'w') as cf:
        config.write(cf)

client = OAuth2Session(client_id=client_id,
                        token=token,
                        auto_refresh_url=spotifyUrlAuthBase+'token',
                        auto_refresh_kwargs=extra,
                        token_updater=save_token)
playlists_url = 'https://api.spotify.com/v1/me/playlists'
print(client.get(playlists_url).json())

# I used the following for the inital authorization of this app

# oauth = OAuth2Session(client_id=client_id,
#                       redirect_uri=redirect_uri,
#                       scope=scope)
#     authorization_url, state = oauth.authorization_url(
#         spotifyUrlAuthBase+'/authorize')
#     print(authorization_url)
#     authorization_response = input('Enter the full callback URL')
#     token = oauth.fetch_token(spotifyUrlAuthBase+'/api/token',
#                               authorization_response=authorization_response,
#                               client_secret=client_secret)
#     config['spotify']['token'] = json.dumps(token)
#     with open(configFile, 'w') as cf:
#             config.write(cf)
