from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class Mixeddit(APIView):

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def put(self, request, subreddit, playlist):
        return Response({'subreddit': subreddit, 'playlist': playlist},
                        status=status.HTTP_200_OK)
