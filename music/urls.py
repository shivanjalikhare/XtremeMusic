from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
	# /music/ ~home page for music
    path('', views.IndexView.as_view(), name='index'),
    
    # /music/71/ (album_id)
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    #/music/album/add/
    re_path(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),

   
]