from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def index(request):
    return Response()


@api_view(['PUT'])
def playlist_replace(request, subreddit, playlist):
    return Response({'subreddit': subreddit, 'playlist': playlist})
