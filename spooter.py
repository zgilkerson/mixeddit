import configparser
import json
from requests_oauthlib import OAuth2Session

class spooter:
    """ Spotify class, reminds me of the scary Spooders """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.configFile = 'config.ini'
        self.config.read(self.configFile)
        client_id = self.config['spotify']['client_id']
        client_secret = self.config['spotify']['client_secret']
        token = json.loads(self.config['spotify']['token'])
        spotifyUrlAuthBase = 'https://accounts.spotify.com/api/token'
        extra = {'client_id': client_id,'client_secret': client_secret}
        self.client = OAuth2Session(client_id=client_id,token=token,
                                    auto_refresh_url=spotifyUrlAuthBase,
                                    auto_refresh_kwargs=extra,token_updater=self.saveToken)
        self.spotifyBaseUrl = 'https://api.spotify.com/v1/'

    def saveToken(self, newToken):
        """ Write the new token to config file """
        self.config['spotify']['token'] = json.dumps(newToken)
        with open(self.configFile, 'w') as cf:
            self.config.write(cf)
    
    def playlistGetAllForCurrentUser(self):
        """ Returns a list of all playlists that belong to the current user """
        playlists_url = self.spotifyBaseUrl+'me/playlists'
        return self.client.get(playlists_url).json()

    def playlistGetId(self, targetPlaylistName):
        """ Get the id of a Spotify Playlist """
        all_playlists = self.playlistGetAllForCurrentUser()
        for playlist in all_playlists['items']:
            if(playlist['name'] == targetPlaylistName):
                return playlist['id']

    def playlistReplace(self, user_id, playlist_id, track_list):
        """ Replace the given playlist with the list of provided tracks """
        replace_url = 'https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks'.format(user_id=user_id, playlist_id=playlist_id)
        payload = { "uris" : track_list }
        self.client.put(replace_url, json=payload)

    def currentUserGetId(self):
        """ Get the id of the current user """
        user_info = self.client.get(self.spotifyBaseUrl+'me').json()
        return user_info['uri'].split('spotify:user:', 1)[1]

    def search(self, query, queryType):
        """ Search Spotify for something """
        search_url = self.spotifyBaseUrl+'search'
        payload = {'q': query, 'type': queryType}
        searchResults = self.client.get(search_url, params=payload).json()
        return searchResults
