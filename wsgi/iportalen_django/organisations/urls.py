__author__ = 'jonathan'
from django.conf.urls import include, url
from .views import (
    organisation,
    edit_organisation,
    all_organisations
)

urlpatterns = [
    url(r'^$', all_organisations, name='all organisations'),
    url(r'^(?P<organisation_name>[^/]+)/$', organisation, name='organisation'),
    url(r'^(?P<organisation_name>[^/]+)/edit/$', edit_organisation, name='edit_organisation'),
]
