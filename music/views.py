from django.http import HttpResponse
from django.shortcuts import render
from .models import Album 

def index(request):
	#get all objects from db
	all_albums = Album.objects.all()
	context = { 'all_albums': all_albums}
	return render(request, 'music/index.html', context)

def detail(request, album_id):
	return HttpResponse("this is detailed view of " + str(album_id) +".")