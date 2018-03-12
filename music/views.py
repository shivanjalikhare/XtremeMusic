from django.http import HttpResponse
from django.template import loader
from .models import Album 

def index(request):
	#get all objects from db
	all_albums = Album.objects.all()
	template = loader.get_template('music/index.html')
	context = {
		'all_albums': all_albums,

	}
	return HttpResponse(template.render(context, request))

def detail(request, album_id):
	return HttpResponse("this is detailed view of " + str(album_id) +".")