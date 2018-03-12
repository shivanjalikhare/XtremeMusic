from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
	# /music/ ~home page for music
    path('', views.index, name='index'),
    
    # /music/71/ (album_id)
    re_path(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
]