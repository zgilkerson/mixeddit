from django.shortcuts import render
from django.http import HttpResponse, Http404


def index(request):
    return HttpResponse('Hello, this is Spotify.index')


def playlist_replace(request, subreddit, playlist):
    # if 'it' in playlist:
        # raise Http404('You playlist has a bad name')
    return HttpResponse('Are you sure you want to replace {playlist} '
                        'with the top of the past week from r/{subreddit}'
                        .format(playlist=playlist, subreddit=subreddit))
