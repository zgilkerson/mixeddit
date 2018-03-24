from django.db import models
from django.utils import timezone


class Song(models.Model):
    artist = models.TextField(default='')
    track = models.TextField(default='')
    uri = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
