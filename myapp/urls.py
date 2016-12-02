from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "myapp"

urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),

    # url = /myapp/album/add/2/
    url(r'album/add/$', views.AlbumCreate.as_view(), name="album-add"),
    url(r'songs/add/(?P<pk>[0-9]+)/$', views.SongCreate.as_view(), name="song-add"),

    # url = /myapp/album/2/
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name="album-update"),

    # url = /myapp/album/2/delete/
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name="album-delete"),
    url(r'detail/(?P<pk>[0-9]+)/delete/$', views.SongDelete.as_view(), name="song-delete"),

    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    #url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    #url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
]
