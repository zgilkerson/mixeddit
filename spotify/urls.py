from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from spotify.views import SpotifyViewSet

router = DefaultRouter()
router.register(r'', SpotifyViewSet, base_name='spotify')

urlpatterns = router.urls
