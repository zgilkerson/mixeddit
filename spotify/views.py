import configparser
from requests_oauthlib import OAuth2Session

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
        scope = 'playlist-read-private, playlist-modify-private, user-read-private'
        return Response(status=status.HTTP_200_OK)
