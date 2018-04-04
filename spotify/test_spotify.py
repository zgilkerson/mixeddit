import configparser
import json
import requests
from spotify.spotify import Spotify
from spotify.spotify_error import SpotifyRunTimeError, SpotifySetUpError
# import unittest
from django.test import TestCase
from unittest.mock import Mock, patch


class MockRequest():

    def __init__(self, response, authorized=True):
        self.response = response
        self.authorized = authorized
        self.http_error_msg = ''

    def get(self):
        return self

    def put(self):
        return self

    def json(self):
        return self.response

    def raise_for_status_response(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason
        self.http_error_msg = u'%s Client Error: %s' % (
            status_code, reason)

    def raise_for_status(self):
        if self.http_error_msg:
            raise requests.exceptions.HTTPError(self.http_error_msg)


class TestSpotify(TestCase):

    maxDiff = None

    @patch('spotify.spotify.OAuth2Session')
    def setUp(self, mock_oauth):
        mock_oauth.return_value = MockRequest("fake response", True)
        self.test_files = 'testFiles/Spotify/'
        ini = self.test_files+'testSpotify.ini'
        config = configparser.ConfigParser()
        config.read(ini)
        self.session = {'token': config['testSpotify']['token']}
        self.spotify = Spotify(self.session, config_file=ini,
                               config_section='testSpotify')

    @patch('spotify.spotify.OAuth2Session')
    def test_init_config_file(self, mock_oauth):
        mock_oauth.return_value = MockRequest("fake response", True)
        ini = self.test_files+'testSpotify.ini'
        config = configparser.ConfigParser()
        config.read(ini)
        client_id = config['testSpotify']['client_id']
        client_secret = config['testSpotify']['client_secret']
        spotify = Spotify(self.session, config_file=ini,
                          config_section='testSpotify')
        self.assertEqual(client_id, spotify.client_id)
        self.assertEqual(client_secret, spotify.client_secret)

    @patch('spotify.spotify.OAuth2Session')
    def test_init_config_not_file(self, mock_oauth):
        ini = 1
        with self.assertRaises(SpotifySetUpError) as e:
            Spotify(self.session, config_file=ini)
        Mock.assert_not_called(mock_oauth)
        self.assertEqual('\'The configuration file needs to be a string or '
                         'path-like object.\'', str(e.exception))

    @patch('spotify.spotify.OAuth2Session')
    def test_init_key_not_in_config(self, mock_oauth):
        ini = self.test_files+'testSpotify.ini'
        with self.assertRaises(SpotifySetUpError) as e:
            Spotify(self.session, config_file=ini,
                    config_section='no_section')
        Mock.assert_not_called(mock_oauth)
        self.assertEqual('\"Could not find key \'no_section\'.\"',
                         str(e.exception))

    @patch('spotify.spotify.OAuth2Session')
    def test_init_wrong_values(self, mock_oauth):
        ini = self.test_files+'testSpotify.ini'
        mock_oauth.return_value = MockRequest("fake response", False)
        with self.assertRaises(SpotifySetUpError) as e:
            Spotify(self.session, config_file=ini,
                    config_section='testSpotify')
        Mock.assert_called_once(mock_oauth)
        self.assertEqual('\'There was a problem with authorization.\'',
                         str(e.exception))

    @patch('spotify.test_spotify.MockRequest.get')
    def test_playlist_get_all(self, mock_oauth):
        with open(self.test_files + 'allPlaylists.json') as json_file:
            testJson = json.load(json_file)
        mock_oauth.return_value = MockRequest(testJson)
        response = self.spotify.playlist_get_all('testUserId')
        mock_oauth.assert_called_once_with(Spotify.BASE_URL+'users/testUserId/'
                                           'playlists')
        self.assertEqual(testJson, response)

    @patch('spotify.test_spotify.MockRequest.get')
    def test_playlist_get_all_error(self, mock_oauth):
        with open(self.test_files + 'error.json') as json_file:
            mock_oauth.return_value = MockRequest(json.load(json_file))
        mock_oauth.return_value.raise_for_status_response(
            400, 'bad request'
        )
        with self.assertRaises(SpotifyRunTimeError) as e:
            self.spotify.playlist_get_all('testUserId')
        mock_oauth.assert_called_once_with(Spotify.BASE_URL+'users/testUserId/'
                                           'playlists')
        self.assertEqual(400, e.exception.error_code)
        self.assertEqual('bad request', e.exception.error_message)
        self.assertEqual('Spotify returned with error code: 400, '
                         'bad request', str(e.exception))

    @patch('spotify.spotify.Spotify.playlist_get_all')
    def test_playlist_get_id(self, mock_method):
        with open(self.test_files+'allPlaylists.json') as json_file:
            mock_method.return_value = json.load(json_file)
        playlist_id = self.spotify.playlist_get_id(
            'xvtx9jvj0ywnfqpma8tyqr37p', 'TopOfShreddit')
        mock_method.assert_called_once_with('xvtx9jvj0ywnfqpma8tyqr37p')
        self.assertEqual('53Y8wT46QIMz5H4WQ8O22c', playlist_id)

    @patch('spotify.spotify.Spotify.playlist_get_all')
    def test_playlist_get_id_empty_items(self, mock_method):
        mock_method.return_value = json.loads('{"items": []}')
        playlist_id = self.spotify.playlist_get_id(
            'xvtx9jvj0ywnfqpma8tyqr37p', 'TopOfShreddit')
        mock_method.assert_called_once_with('xvtx9jvj0ywnfqpma8tyqr37p')
        self.assertEqual(None, playlist_id)

    @patch('spotify.spotify.Spotify.playlist_get_all')
    def test_playlist_get_id_no_name_match(self, mock_method):
        with open(self.test_files+'allPlaylists.json') as json_file:
            mock_method.return_value = json.load(json_file)
        playlist_id = self.spotify.playlist_get_id(
            'xvtx9jvj0ywnfqpma8tyqr37p', 'BottomOfShreddit')
        mock_method.assert_called_once_with('xvtx9jvj0ywnfqpma8tyqr37p')
        self.assertEqual(None, playlist_id)

    @patch('spotify.test_spotify.MockRequest.put')
    def test_playlist_replace(self, mock_oauth):
        # Testament - Practice What You Preach
        # Rage Against The Machine - Testify
        # Run The Jewels - Ddfh
        track_list = ['spotify:track:1KmX2Q8IwwLY2AMIMOmYlw',
                      'spotify:track:7lmeHLHBe4nmXzuXc0HDjk',
                      'spotify:track:7vAPdj763w31JAjcDW7Q2r']
        self.spotify.playlist_replace('testUserId', 'testPlaylistId',
                                      track_list)
        mock_oauth.assert_called_once_with(Spotify.BASE_URL+'users/testUserId/'
                                           'playlists/testPlaylistId/tracks',
                                           json={'uris': track_list})

    @patch('spotify.test_spotify.MockRequest.put')
    def test_playlist_replace_http_error(self, mock_oauth):
        with open(self.test_files + 'error.json') as json_file:
            mock_oauth.return_value = MockRequest(json.load(json_file))
        mock_oauth.return_value.raise_for_status_response(
            400, 'bad request'
        )
        with self.assertRaises(SpotifyRunTimeError) as e:
            self.spotify.playlist_replace('testUserId', 'testPlaylistId', [])
        mock_oauth.assert_called_once_with(Spotify.BASE_URL+'users/testUserId/'
                                           'playlists/testPlaylistId/tracks',
                                           json={'uris': []})
        self.assertEqual(400, e.exception.error_code)
        self.assertEqual('bad request', e.exception.error_message)
        self.assertEqual('Spotify returned with error code: 400, '
                         'bad request', str(e.exception))

    @patch('spotify.test_spotify.MockRequest.get')
    def test_user_get_current_user_id(self, mock_oauth):
        with open(self.test_files+'currentUserProfile.json') as json_file:
            mock_oauth.return_value = MockRequest(json.load(json_file))
        user_id = self.spotify.user_get_current_user_id()
        mock_oauth.assert_called_once_with(Spotify.BASE_URL+'me')
        self.assertEqual('xvtx9jvj0ywnfqpma8tyqr37p', user_id)

    @patch('spotify.test_spotify.MockRequest.get')
    def test_user_get_current_user_id_error(self, mock_oauth):
        with open(self.test_files + 'error.json') as json_file:
            mock_oauth.return_value = MockRequest(json.load(json_file))
        mock_oauth.return_value.raise_for_status_response(
            400, 'bad request'
        )
        with self.assertRaises(SpotifyRunTimeError) as e:
            self.spotify.user_get_current_user_id()
        mock_oauth.assert_called_once_with(Spotify.BASE_URL+'me')
        self.assertEqual(400, e.exception.error_code)
        self.assertEqual('bad request', e.exception.error_message)
        self.assertEqual('Spotify returned with error code: 400, '
                         'bad request', str(e.exception))

    @patch('spotify.test_spotify.MockRequest.get')
    def test_search(self, mock_oauth):
        with open(self.test_files + 'allPlaylists.json') as json_file:
            testJson = json.load(json_file)
        mock_oauth.return_value = MockRequest(testJson)
        query = 'sabaton'
        query_type = 'artist'
        response = self.spotify.search(query, query_type)
        mock_oauth.assert_called_once_with(Spotify.BASE_URL+'search',
                                           params={'q': query,
                                                   'type': query_type})
        self.assertEqual(testJson, response)

    @patch('spotify.test_spotify.MockRequest.get')
    def test_search_error(self, mock_oauth):
        with open(self.test_files + 'error.json') as json_file:
            mock_oauth.return_value = MockRequest(json.load(json_file))
        mock_oauth.return_value.raise_for_status_response(
            400, 'bad request'
        )
        query = 'sabaton'
        query_type = 'artist'
        with self.assertRaises(SpotifyRunTimeError) as e:
            self.spotify.search(query, query_type)
        mock_oauth.assert_called_once_with(Spotify.BASE_URL+'search',
                                           params={'q': query,
                                                   'type': query_type})
        self.assertEqual(400, e.exception.error_code)
        self.assertEqual('bad request', e.exception.error_message)
        self.assertEqual('Spotify returned with error code: 400, '
                         'bad request', str(e.exception))
