from django.db import models


class Song(models.Model):
    artist = models.TextField(default='')
    track = models.TextField(default='')
    uri = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ('Artist: {artist} Track: {track} Uri: {uri}'
                .format(artist=self.artist, track=self.track, uri=self.uri))
