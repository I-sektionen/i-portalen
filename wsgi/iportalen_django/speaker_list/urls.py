from django.conf.urls import url, include
from . import views

app_name = 'speaker_list'


speaker_list_patterns = [
    url(r'^(?P<pk>[0-9]+)/administer/speaker/$',                   view=views.administer_speaker_list,   name="administer speaker list"),
    url(r'^(?P<pk>[0-9]+)/administer/speaker/display/$',           view=views.speaker_list_display,      name="speaker display"),
    url(r'^(?P<pk>[0-9]+)/administer/speaker/api/$',               view=views.speaker_list,              name="speaker api"),
    url(r'^(?P<pk>[0-9]+)/user_add_self_speech_list/$', view=views.speaker_list_user_add_self, name="add user speech nr list"),
    url(r'^(?P<pk>[0-9]+)/user_remove_self_speech_list/$', view=views.speaker_list_user_remove_self, name="remove user speech nr list"),
]

urlpatterns = [url(r'^', include(speaker_list_patterns, namespace=app_name))]