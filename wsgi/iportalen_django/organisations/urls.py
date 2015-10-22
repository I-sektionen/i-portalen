__author__ = 'jonathan'
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.all_organisations, name='all organisations'),
    url(r'^(?P<organisation_name>[^/]+)/$', views.organisation, name='organisation'),
    url(r'^(?P<organisation_name>[^/]+)/edit/$', views.edit_organisation, name='edit organisation'),
]
