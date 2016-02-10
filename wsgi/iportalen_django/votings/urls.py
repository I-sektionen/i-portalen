from django.conf.urls import url, include
from . import views

app_name = "votings"

voting_patterns = [
    url(r'^$',                                           view=views.votings,           name='votings'),
    url(r'^(?P<qg_pk>[0-9]+)/$',                         view=views.question_group,    name='question group'),
    url(r'^(?P<qg_pk>[0-9]+)/(?P<q_pk>[0-9]+)/$',        view=views.question_details,  name='question'),
    url(r'^(?P<qg_pk>[0-9]+)/(?P<q_pk>[0-9]+)/result/$', view=views.question_result,   name='result'),
    url(r'^create/$',                                    view=views.create,            name='create'),
    url(r'^event/create/(?P<event_pk>[0-9]+)/$',         view=views.create_from_event, name='create from event'),
    url(r'^event/admin/(?P<event_pk>[0-9]+)/$',          view=views.admin_from_event,  name='admin from event'),
    url(r'^event/(?P<event_pk>[0-9]+)/$',                view=views.get_from_event,    name='get from event'),
]

urlpatterns = [url(r'^', include(voting_patterns, namespace=app_name))]
