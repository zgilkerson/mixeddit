import configparser
import json
import requests
import logging

from rest_framework import status

from requests_oauthlib import OAuth2Session

from spotify.spotify_error import SpotifySetUpError, SpotifyRunTimeError
from spotify.models import Song

LOGGER = logging.getLogger(__name__)


class Spotify:
    """Class for interacting with the Spotify API."""

    BASE_URL = 'https://api.spotify.com/v1/'

    def __init__(self, session, config_file='spotify.ini',
                 config_section='spotify'):
        self.session = session
        spotify_auth_url = 'https://accounts.spotify.com/api/token'
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.config_section = config_section
        try:
            self.config.read(self.config_file)
            self.client_id = self.config[self.config_section]['client_id']
            self.client_secret = (self.config[self.config_section]
                                  ['client_secret'])
        except TypeError as e:
            raise SpotifySetUpError('The configuration file needs to be a '
                                    'string or path-like object.')
        except KeyError as e:
            raise SpotifySetUpError('Could not find key {}.'.format(e))
        extra = {'client_id': self.client_id,
                 'client_secret': self.client_secret}
        self.client = OAuth2Session(client_id=self.client_id,
                                    token=self.session['token'],
                                    auto_refresh_url=spotify_auth_url,
                                    auto_refresh_kwargs=extra,
                                    token_updater=self.save_token)
        # Check if client was successfully set-up
        if not self.client.authorized:
            raise SpotifySetUpError('There was a problem with authorization.')

    def save_token(self, new_token):
        """Writes the new token to the config file."""

        self.session['token'] = new_token

    def playlist_get_all(self, user_id, offset=0):
        """Returns a list of all playlists that belong to the user."""

        playlists_url = self.BASE_URL+'users/{}/playlists'.format(user_id)
        payload = {'offset': offset, 'limit': 50}
        response = self.client.get(playlists_url, params=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise SpotifyRunTimeError(response.status_code, response.reason)
        return response.json()

    def playlist_get_id(self, user_id, target_playlist_name):
        """Returns the id of the playlist if found under the user
        or None if not found."""

        offset = 0
        all_playlists = self.playlist_get_all(user_id, offset)
        while all_playlists['items']:
            for playlist in all_playlists['items']:
                if playlist['name'] == target_playlist_name:
                    return playlist['id']
            offset += 50
            all_playlists = self.playlist_get_all(user_id, offset)

    def playlist_replace(self, playlist, mixeddit_list,
                         create_playlist, create_public):
        """Replaces the given playlist with the list of provided tracks."""
        user_id = self.user_get_current_user_id()
        playlist_id = self.playlist_get_id(user_id, playlist)
        if playlist_id is None:
            if create_playlist:
                payload = {
                    'name': playlist,
                    'public': create_public
                }
                create_url = self.BASE_URL+'users/{}/playlists'.format(user_id)
                response = self.client.post(create_url, json=payload)
                playlist_id = response['id']
            else:
                raise SpotifyRunTimeError(status.HTTP_404_NOT_FOUND,
                                          'invalid playlist')
        track_uri_list = []
        for reddit_track in mixeddit_list:
            try:
                track_uri = Song.objects.get(  # pylint: disable=E1101
                    artist=reddit_track.artist,
                    track=reddit_track.track).uri
                track_uri_list.append(track_uri)
            except Song.DoesNotExist:  # pylint: disable=E1101
                try:
                    search_results = self.search(reddit_track.track, 'track')
                    try:
                        for spotify_track in search_results['tracks']['items']:
                            if (spotify_track['artists'][0]['name'].lower() ==
                                    reddit_track.artist):
                                Song(artist=reddit_track.artist,
                                     track=reddit_track.track,
                                     uri=spotify_track['uri']).save()
                                track_uri_list.append(spotify_track['uri'])
                                break
                    except KeyError:
                        pass
                except SpotifyRunTimeError:
                    pass

        replace_url = (''.join([self.BASE_URL, 'users/{user_id}/playlists/'
                       '{playlist_id}/tracks'])
                       .format(user_id=user_id, playlist_id=playlist_id))
        payload = {'uris': track_uri_list}
        response = self.client.put(replace_url, json=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise SpotifyRunTimeError(response.status_code, response.reason)

    def user_get_current_user(self):
        """Returns current user information."""

        response = self.client.get(self.BASE_URL+'me')
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise SpotifyRunTimeError(response.status_code, response.reason)
        response = response.json()
        return response

    def user_get_current_user_id(self):
        """Returns the id of the current user."""

        response = self.user_get_current_user()
        return response['uri'].split('spotify:user:', 1)[1]

    def search(self, query, query_type):
        """Search Spotify for something."""

        search_url = self.BASE_URL+'search'
        payload = {'q': query, 'type': query_type}
        response = self.client.get(search_url, params=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise SpotifyRunTimeError(response.status_code, response.reason)
        return response.json()
