from django.conf.urls import url, include
from . import views

app_name = "votings"

voting_patterns = [
    url(r'^$',                                           view=views.votings,          name='votings'),
    url(r'^(?P<qg_pk>[0-9]+)/$',                         view=views.question_group,   name='question group'),
    url(r'^(?P<qg_pk>[0-9]+)/(?P<q_pk>[0-9]+)/$',        view=views.question_details, name='question'),
    url(r'^(?P<qg_pk>[0-9]+)/(?P<q_pk>[0-9]+)/result/$', view=views.question_result,  name='result'),
]

urlpatterns = [url(r'^', include(voting_patterns, namespace=app_name))]