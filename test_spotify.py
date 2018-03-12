import json
from spotify import Spotify
from spotify_error import SpotifyRunTimeError, SpotifySetUpError
import unittest
from unittest.mock import Mock, patch


class MockRequest():

    def get(self, URL):
        return "get"


class TestSpotify(unittest.TestCase):

    def setUp(self):
        self.spotify = Spotify()
        self.test_files = 'testFiles/Spotify/'

    @patch('spotify.OAuth2Session')
    def test_init_config_file(self, mock_oauth):
        mock_oauth.return_value = MockRequest()
        ini = self.test_files+'testSpotify.ini'
        Spotify(spotify_config_file=ini,
                spotify_section_title='testSpotify')
        Mock.assert_called_once(mock_oauth)
        self.assertTrue(True)

    @unittest.skip('work in progress')
    @patch('spotify.OAuth2Session')
    def test_init_config_not_file(self):
        ini = 1
        with self.assertRaises(SpotifySetUpError) as e:
            Spotify(spotify_config_file=ini)
        # self.assertEqual()

    @patch('spotify.Spotify.playlist_get_all')
    def test_playlist_get_id_for_current_user(self, mock_method):
        with open(self.test_files+'mockAllPlaylists.json') as json_file:
            mock_method.return_value = json.load(json_file)
        playlist_id = self.spotify.playlist_get_id(
            'xvtx9jvj0ywnfqpma8tyqr37p', 'TopOfShreddit')
        self.assertEqual('53Y8wT46QIMz5H4WQ8O22c', playlist_id)

if __name__ == '__main__':
    unittest.main()
