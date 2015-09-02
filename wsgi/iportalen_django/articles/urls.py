from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.all_articles, name='articles'),
    url(r'^(?P<article_id>[0-9]+)/$', views.single_article, name='article'),
    url(r'create/$', views.create_or_modify_article, name='create article'),
    url(r'^(?P<article_id>[0-9]+)/edit/$', views.create_or_modify_article, name='edit article'),

]
