from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


class MixedditViewSet(viewsets.ViewSet):
    parser_classes = (JSONParser,)

    @detail_route(methods=['put'])
    def playlist_replace(self, request, pk):
        return Response(request.data, status=status.HTTP_200_OK)