from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout #verifies if user exists, and attaches session id
from django.views import generic
from django.db.models import Q
from django.views.generic import View
from .models import Album, Song
from .forms import UserForm, SongForm

# class IndexView(generic.ListView):
#     template_name = "myapp/index.html"
#     context_object_name = "all_albums"
#
#     def get_queryset(self):
#         return Album.objects.all()

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'myapp/login.html')
    else:
        print request.user
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'myapp/index.html', {
                'all_albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'myapp/index.html', {'all_albums': albums})

# def songs(request):
#     albums = Album.objects.all()
#     Song.objects.order_by('album')
#     songs = Song.objects.all()
#
#     return render(request, 'myapp/songs.html', {"all_songs":songs, "all_albums":albums})

def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'myapp/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        song_results = Song.objects.all()
        albums = Album.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'myapp/index.html', {
                'all_albums': albums,
                'songs': song_results,
            })
        return render(request, 'myapp/songs.html', {
            'all_songs': users_songs.order_by('song_title').order_by('album'),
            'filter_by': filter_by,
        })

class DetailView(generic.DetailView):
    model = Album
    template_name = "myapp/detail.html"


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('myapp:index')


class SongCreate(CreateView):
    model = Song
    fields = ['album', 'song_title', 'file_type']


class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('myapp:index')


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'myapp/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        #song.audio_file = request.FILES['audio_file']
        # file_type = "song.audio_file.url.split('.')[-1]"
        # file_type = file_type.lower()
        # if file_type not in AUDIO_FILE_TYPES:
        #     context = {
        #         'album': album,
        #         'form': form,
        #         'error_message': 'Audio file must be WAV, MP3, or OGG',
        #     }
        #     return render(request, 'myapp/create_song.html', context)

        song.save()
        return render(request, 'myapp/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'myapp/create_song.html', context)

def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'myapp/detail.html', {'album': album})


class UserFormView(View):
    form_class = UserForm
    template_name = 'myapp/registration_form.html'

    # Displays blank form to new user without an account
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    # Process form data to create a new User
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('myapp:index')


        return render(request, self.template_name, {'form':form})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'myapp/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'myapp/index.html', {'all_albums': albums})
            else:
                return render(request, 'myapp/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'myapp/login.html', {'error_message': 'Invalid login'})
    return render(request, 'myapp/login.html')
