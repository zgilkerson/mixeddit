import configparser
import json
from requests_oauthlib import OAuth2Session
from spotify_error import SpotifySetUpError


BASE_URL = 'https://api.spotify.com/v1/'


class Spotify:
    """Class for interacting with the Spotify API."""

    def __init__(self, spotify_config_file='spotify.ini',
                 spotify_section_title='spotify'):
        spotify_auth_url = 'https://accounts.spotify.com/api/token'
        self.config = configparser.ConfigParser()
        self.config_file = spotify_config_file
        self.config_section = spotify_section_title
        try:
            self.config.read(self.config_file)
            client_id = self.config[self.config_section]['client_id']
            client_secret = self.config[self.config_section]['client_secret']
            token = json.loads(self.config[self.config_section]['token'])
        except TypeError as e:
            raise SpotifySetUpError('The configuration file needs to be a '
                                    'string or file pointer')
        except KeyError as e:
            raise SpotifySetUpError('Could not find key {}'.format(e))
        extra = {'client_id': client_id, 'client_secret': client_secret}
        self.client = OAuth2Session(client_id=client_id, token=token,
                                    auto_refresh_url=spotify_auth_url,
                                    auto_refresh_kwargs=extra,
                                    token_updater=self.save_token)
        # Check if client was successfully set-up
        try:
            self.client.get(BASE_URL+'me')
        except Exception:
            raise SpotifySetUpError("There was a problem with authorization")

    def save_token(self, new_token):
        """Writes the new token to the config file."""

        self.config[self.config_section]['token'] = json.dumps(new_token)
        with open(self.config_file, 'w') as cf:
            self.config.write(cf)

    def playlist_get_all(self, user_id):
        """Returns a list of all playlists that belong to the user."""

        playlists_url = BASE_URL+'users/{}/playlists'.format(user_id)
        return self.client.get(playlists_url).json()

    def playlist_get_id(self, user_id, target_playlist_name):
        """Returns the id of the playlist if found under the user."""

        all_playlists = self.playlist_get_all(user_id)
        for playlist in all_playlists['items']:
            if(playlist['name'] == target_playlist_name):
                return playlist['id']

    def playlist_replace(self, user_id, playlist_id, track_list):
        """Replaces the given playlist with the list of provided tracks."""

        replace_url = ''.join([BASE_URL, 'users/{user_id}/playlists/'
                              '{playlist_id}/tracks'])\
                        .format(user_id=user_id, playlist_id=playlist_id)
        payload = {"uris": track_list}
        self.client.put(replace_url, json=payload)

    def user_get_current_user_id(self):
        """Returns the id of the current user."""

        user_info = self.client.get(BASE_URL+'me').json()
        return user_info['uri'].split('spotify:user:', 1)[1]

    def search(self, query, query_type):
        """Search Spotify for something."""

        search_url = BASE_URL+'search'
        payload = {'q': query, 'type': query_type}
        results = self.client.get(search_url, params=payload).json()
        return results
