import json
from spotify import Spotify
import unittest
from unittest.mock import Mock, patch
from requests_oauthlib import OAuth2Session


class TestSpotify(unittest.TestCase):

    def setUp(self):
        self.spotify = Spotify()
        self.test_files = 'testFiles/Spotify/'

    def test_init_config_file(self):
        ini = self.test_files+'testSpotify.ini'
        spotify = Spotify(spotify_config_file=ini,
                          spotify_section_title='testSpotify')
        spotify.client.close()
        self.assertTrue(True)
    
    @patch('spotify.Spotify.playlist_get_all')
    def test_playlist_get_id_for_current_user(self, mock_method):
        with open(self.test_files+'mockAllPlaylists.json') as json_file:
            mock_method.return_value = json.load(json_file)
        playlist_id = self.spotify.playlist_get_id(
            'xvtx9jvj0ywnfqpma8tyqr37p', 'TopOfShreddit')
        self.assertEqual('53Y8wT46QIMz5H4WQ8O22c', playlist_id)

if __name__ == '__main__':
    unittest.main()
