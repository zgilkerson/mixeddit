import configparser
from requests_oauthlib import OAuth2Session
import logging

from django.shortcuts import redirect

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse

import prawcore.exceptions

from reddit.reddit import Reddit

from spotify.spotify import Spotify
from spotify.spotify_error import SpotifyRunTimeError, SpotifySetUpError

logger = logging.getLogger(__name__)


class SpotifyViewSet(viewsets.ViewSet):
    parser_classes = (JSONParser,)

    @action(methods=['get'], detail=False)
    def login(self, request, *args, **kwargs):
        scope = ('playlist-read-private, playlist-modify-public, '
                 'playlist-modify-private')
        config = configparser.ConfigParser()
        config.read('spotify.ini')
        client_id = config['spotify']['client_id']
        redirect_uri = 'https://localhost/api/spotify/callback'
        oauth = OAuth2Session(client_id=client_id,
                              redirect_uri=redirect_uri,
                              scope=scope)
        auth_url, state = oauth.authorization_url(
            'https://accounts.spotify.com/authorize')
        request.session['oauth_state'] = state
        return redirect(auth_url)

    @action(methods=['get'], detail=False)
    def callback(self, request, *args, **kwargs):
        config = configparser.ConfigParser()
        config.read('spotify.ini')
        client_id = config['spotify']['client_id']
        client_secret = config['spotify']['client_secret']
        redirect_uri = 'https://localhost/api/spotify/callback'
        oauth = OAuth2Session(client_id=client_id,
                              redirect_uri=redirect_uri,
                              state=request.session['oauth_state'])
        token_uri = 'https://accounts.spotify.com/api/token'
        token = oauth.fetch_token(
            token_uri,
            authorization_response=request.build_absolute_uri(),
            client_secret=client_secret)
        request.session['token'] = token
        return redirect('/')

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        spotify = Spotify(request.session)
        return Response(spotify.user_get_current_user(),
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def check_logged_in(self, request, *args, **kwargs):
        try:
            request.session['token']
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['put'], detail=False)
    def playlist_replace(self, request, *args, **kwargs):
        try:
            request.session['token']
        except KeyError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        subreddit = request.data['subreddit']
        playlist = request.data['playlist']
        try:
            mixeddit_list = Reddit.parseSubreddit(subreddit)
        except prawcore.exceptions.PrawcoreException:
            return Response({'error': {
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'invalid subreddit'
            }},
                            status=status.HTTP_404_NOT_FOUND)
        spotify = Spotify(request.session)
        try:
            spotify.playlist_replace(playlist, mixeddit_list)
        except SpotifyRunTimeError as e:
            return Response({'error': {
                'status': e.error_code,
                'message': e.error_message
            }}, status=e.error_code)
        return Response(request.data, status=status.HTTP_200_OK)
