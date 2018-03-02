import json
from spooter import spooter
import unittest
from unittest.mock import Mock, patch
from requests_oauthlib import OAuth2Session

class test_spooter(unittest.TestCase):

    def setUp(self):
        self.spotify = spooter()
    
    def test_init(self):
        spotify = spooter()
        self.assertIsNotNone(spotify.config)
        self.assertEqual(spotify.configFile, 'config.ini')
        self.assertIsNotNone(spotify.client)
        self.assertEqual(spotify.spotifyBaseUrl, 'https://api.spotify.com/v1/')

    @patch('spooter.OAuth2Session.get')
    def test_playlistGetAll(self, mock_get):
        fakeJson = {
            "items" : [{
                "name": "TopOfShreddit",
                "id": "666"
            }, {
                "name": "BottomOfShreddit",
                "id": "555"
            }, {
                "name": "MiddleOfShreddit",
                "id": "5.5.5"
            }]
        }
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = fakeJson
        allPlaylists = self.spotify.playlistGetAll()
        self.assertTrue(type(allPlaylists) is dict)

    @patch('spooter.OAuth2Session.get')
    def test_mocking(self, mock_get):
        mock_get.return_value.ok = True
        response = self.spotify.mocking()
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()
