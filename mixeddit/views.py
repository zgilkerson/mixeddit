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

    @detail_route(methods=['put'])
    def playlist_replace(self, request, pk):
        reddit = praw.Reddit('mixeddit')
        if reddit.read_only is not True:
            exit()
        mixeddit_list = []
        for submission in reddit.subreddit(request.data['subreddit']
                                           ).top('week', limit=100):
            parsedTitle = Mixeddit(submission.title)
            if parsedTitle.valid:
                mixeddit_list.append(parsedTitle)
        spotify = Spotify(request.session)
        user_id = spotify.user_get_current_user_id()
        playlist_id = spotify.playlist_get_id(user_id,
                                              request.data['playlist'])
        track_uri_list = []
        for reddit_track in mixeddit_list:
            try:
                search_results = spotify.search(reddit_track.track, 'track')
                try:
                    for spotify_track in search_results['tracks']['items']:
                        if (spotify_track['artists'][0]['name'].lower() ==
                                reddit_track.artist.lower()):
                            track_uri_list.append(spotify_track['uri'])
                            break
                except KeyError:
                    pass
            except SpotifyRunTimeError:
                pass
        spotify.playlist_replace(user_id, playlist_id, track_uri_list)
        return Response(request.data, status=status.HTTP_200_OK)
