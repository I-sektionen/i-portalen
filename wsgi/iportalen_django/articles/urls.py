from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<article_id>[0-9]+)/$', views.single_article, name='article')
]
