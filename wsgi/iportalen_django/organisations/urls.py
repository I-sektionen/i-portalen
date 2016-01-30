from django.conf.urls import url, include
from . import views

app_name = 'organisations'

organisation_patterns = [
    url(r'^create/$',                               view=views.add_organisation,  name='create'),
    url(r'^(?P<organisation_name>[^/]+)/$',         view=views.organisation,      name='organisation'),
    url(r'^(?P<organisation_name>[^/]+)/edit/$',    view=views.edit_organisation, name='edit'),
    url(r'^(?P<organisation_name>[^/]+)/members/$', view=views.edit_memebers,     name='edit organisation members'),
]

urlpatterns = [url(r'^', include(organisation_patterns, namespace=app_name))]
