from django.conf.urls import url, include
from . import views

app_name = 'thesis_portal'

thesis_patterns = [
    url(r'^$', view=views.thesis_portal, name='thesis_portal'),
    url(r'^article/(?P<pk>[0-9]+)/$', view=views.single_article, name='thesis_article')
]

urlpatterns = [url(r'^', include(thesis_patterns, namespace=app_name))]
