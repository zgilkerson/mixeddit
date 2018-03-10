import json
from spotify import Spotify
import unittest
from unittest.mock import Mock, patch
from requests_oauthlib import OAuth2Session


class Test_Spotify(unittest.TestCase):

    def setUp(self):
        self.spotify = Spotify()
        self.test_json_folder = 'testJson/Spotify/'

    @patch('spotify.Spotify.playlist_get_all')
    def test_playlist_get_id_for_current_user(self, mock_method):
        with open(self.test_json_folder+'mockAllPlaylists.json') as json_file:
            mock_method.return_value = json.load(json_file)
        playlist_id = self.spotify.playlist_get_id(
            'xvtx9jvj0ywnfqpma8tyqr37p', 'TopOfShreddit')
        self.assertEqual('53Y8wT46QIMz5H4WQ8O22c', playlist_id)

if __name__ == '__main__':
    unittest.main()
