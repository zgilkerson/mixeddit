import json
from spooter import spooter
import unittest
from unittest.mock import Mock, patch
from requests_oauthlib import OAuth2Session

class test_spooter(unittest.TestCase):

    def setUp(self):
        self.spotify = spooter()
        self.testJsonFP = 'testJson/Spotify/'
    
    @patch('spooter.spooter.playlistGetAllForCurrentUser')
    def test_playlistGetId(self, mock_method):
        with open(self.testJsonFP+'mockAllPlaylists.json') as testJson:
            mock_method.return_value = json.load(testJson)
        playlistId = self.spotify.playlistGetId('TopOfShreddit')
        self.assertEqual('53Y8wT46QIMz5H4WQ8O22c', playlistId)

if __name__ == '__main__':
    unittest.main()
