"""mixeddit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from .views import MixedditViewSet

router = DefaultRouter()
router.register(r'', MixedditViewSet, base_name='api')

urlpatterns = [
    url(r'^', include(router.urls))
] + staticfiles_urlpatterns()

if settings.ADMIN_ENABLED:
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
    ]
