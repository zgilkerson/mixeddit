from django.conf.urls import url

from . import views

app_name = 'spotify'
urlpatterns = [
    # ex: /spotify/
    url(r'^$', views.index, name='index'),
    # ex: /spotify/metal/TopOfShreddit
    url(r'^(?P<subreddit>[a-zA-Z0-9_]+)/(?P<playlist>[a-zA-Z0-9_]+)/?$',
        views.playlist_replace, name='playlist_replace'),
]
