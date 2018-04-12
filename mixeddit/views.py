from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

import praw

from mixeddit.mixeddit import Mixeddit

from spotify.spotify import Spotify
from spotify.spotify_error import SpotifyRunTimeError, SpotifyRunTimeError


class MixedditViewSet(viewsets.ViewSet):
    parser_classes = (JSONParser,)
