from django.conf.urls import url, include
from . import views

app_name = 'fika_penalty'

fika_patterns = [
    url(r'^all/$', view=views.all_penalties,     name='all penalties'),
    url(r'^(?P<organisation_name>[^/]+)/$', view=views.penalties_per_organisation,     name='organisation penalties'),
]

urlpatterns = [url(r'^', include(fika_patterns, namespace=app_name))]