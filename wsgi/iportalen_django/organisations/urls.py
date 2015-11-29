from django.conf.urls import url
from .views import (
    organisation,
    edit_organisation,
    add_organisation
)

urlpatterns = [
    url(r'^add/$', add_organisation, name='add organisation'),
    url(r'^(?P<organisation_name>[^/]+)/$', organisation, name='organisation'),
    url(r'^(?P<organisation_name>[^/]+)/edit/$', edit_organisation, name='edit_organisation'),
]
