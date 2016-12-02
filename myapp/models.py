from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.urlresolvers import reverse



class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    artist = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    logo = models.FileField()

    def get_absolute_url(self):
        return reverse('myapp:detail', kwargs={'pk':self.pk})

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)



class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10, default="mp3")
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)


    def __str__(self):
        return self.song_title

    def get_absolute_url(self):
        return reverse('myapp:detail', kwargs={'pk':self.album.pk})
