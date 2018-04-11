from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
	# /music/ ~home page for music
    path('', views.IndexView.as_view(), name='index'),

    re_path(r'^register/$', views.UserFormView.as_view(), name='register'),
    
    # /music/71/ (album_id)
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    #/music/album/add/
    re_path(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),

	#/music/album/2/ update
    re_path(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
   
    #/music/album/2/ delete
    re_path(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),

    re_path(r'^logout_user/$', views.logout_user, name='logout_user'),

    re_path(r'^login_user/$', views.login_user, name='login_user'),

]