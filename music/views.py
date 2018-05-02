from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Album
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth import logout

class IndexView(generic.ListView):
	template_name = 'music/index.html'
	context_object_name = 'all_albums'

	def get_queryset(self):
		return Album.objects.all()

class DetailView(generic.DetailView):
	model = Album
	template_name = "music/detail.html"
	
		
class AlbumCreate(CreateView):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)

class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
	model = Album
	success_url = reverse_lazy('music:index')

class UserFormView(View):
	form_class = UserForm
	template_name = 'music/registration_form.html'

	#display a blank form (new user)
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	#process form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			#cleaned (normalised data)
			username = form.clean_data['username']
			password = form.clean_data['password']
			user.set_password(password)
			user.save()
		
		#returns User objects if credentials are correct
		user = authenticate(username-username, password=password)

		if user is not None:

			if user.is_active:

				login(request, user)
				return redirect('music:index')

		return render(request, self.template_name, {'form': form})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
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
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })