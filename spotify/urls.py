from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from spotify.views import SpotifyViewSet

# router = DefaultRouter()
# router.register(r'', SpotifyViewSet, base_name='spotify')

# urlpatterns = [
#     url(r'^', include(router.urls)),
# ]

spotify_me = SpotifyViewSet.as_view({
    'get': 'me',
})

spotify_you = SpotifyViewSet.as_view({
    'get': 'you',
})

urlpatterns = [
    url(r'^spotify/me', spotify_me, name='spotify-me'),
    url(r'^spotify/you', spotify_you, name='spotify-you'),
]
