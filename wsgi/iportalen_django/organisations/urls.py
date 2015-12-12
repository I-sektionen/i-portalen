from django.conf.urls import url
from .views import (
    organisation,
    edit_organisation,
    add_organisation,
    edit_memebers
)

urlpatterns = [
    url(r'^create/$', add_organisation, name='create'),
    url(r'^(?P<organisation_name>[^/]+)/$', organisation, name='organisation'),
    url(r'^(?P<organisation_name>[^/]+)/edit/$', edit_organisation, name='edit'),
    url(r'^(?P<organisation_name>[^/]+)/members/$', edit_memebers, name='edit_organisation_members'),
]
