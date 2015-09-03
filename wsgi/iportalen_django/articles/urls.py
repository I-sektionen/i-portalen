from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.all_articles, name='articles'),
    url(r'^(?P<article_id>[0-9]+)/$', views.single_article, name='article'),
    url(r'^create/$', views.create_or_modify_article, name='create article'),
    url(r'^(?P<article_id>[0-9]+)/edit/$', views.create_or_modify_article, name='edit article'),
    url(r'^approved/$', views.all_approved_articles, name='approved articles'),
    url(r'^unapproved/$', views.all_unapproved_articles, name='unapproved articles'),
    url(r'^(?P<article_id>[0-9]+)/approve$', views.approve_article, name='approve article'),
]
