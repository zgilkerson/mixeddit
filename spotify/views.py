import configparser
from requests_oauthlib import OAuth2Session

from django.http import HttpResponseRedirect

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from spotify.spotify import Spotify
from spotify.spotify_error import SpotifyRunTimeError, SpotifyRunTimeError


class SpotifyViewSet(viewsets.ViewSet):
    parser_classes = (JSONParser,)

    @detail_route(methods=['get'])
    def login(self, request, pk):
        scope = ('playlist-read-private, playlist-modify-public, '
                 'playlist-modify-private')
        config = configparser.ConfigParser()
        config.read('spotify.ini')
        client_id = config['spotify']['client_id']
        redirect_uri = 'https://localhost:8000/spotify/callback'
        oauth = OAuth2Session(client_id=client_id,
                              redirect_uri=redirect_uri,
                              scope=scope)
        auth_url, state = oauth.authorization_url(
            'https://accounts.spotify.com/authorize')
        request.session['oauth_state'] = state
        return HttpResponseRedirect(auth_url)

    @detail_route(methods=['get'])
    def callback(self, request, pk):
        config = configparser.ConfigParser()
        config.read('spotify.ini')
        client_id = config['spotify']['client_id']
        client_secret = config['spotify']['client_secret']
        redirect_uri = 'https://localhost:8000/spotify/callback'
        oauth = OAuth2Session(client_id=client_id,
                              redirect_uri=redirect_uri,
                              state=request.session['oauth_state'])
        token_uri = 'https://accounts.spotify.com/api/token'
        token = oauth.fetch_token(
            token_uri,
            authorization_response=request.build_absolute_uri(),
            client_secret=client_secret)
        request.session['token'] = token
        BASE_URL = 'https://api.spotify.com/v1/'
        response = oauth.get(BASE_URL+'me').json()
        return Response(response, status=status.HTTP_200_OK)
