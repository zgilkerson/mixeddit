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
from django.views.generic import RedirectView, TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from .views import MixedditViewSet

router = DefaultRouter()
router.register(r'', MixedditViewSet, base_name='api')

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^', include(router.urls)),
    url(r'^api/spotify/', include('spotify.urls')),
    url(r'^static/$', TemplateView.as_view(template_name="index.html")),
    url(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
        RedirectView.as_view(url='/static/%(path)s', permanent=False)),
] + staticfiles_urlpatterns()

if settings.ADMIN_ENABLED:
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
    ]
