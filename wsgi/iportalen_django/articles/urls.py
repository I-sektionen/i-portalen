from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.all_articles, name='articles'),
    url(r'^(?P<article_id>[0-9]+)/$', views.single_article, name='article'),
    url(r'^create/$', views.create_or_modify_article, name='create article'),
    url(r'^(?P<article_id>[0-9]+)/edit/$', views.create_or_modify_article, name='edit article'),
    url(r'^unapproved/$', views.all_unapproved_articles, name='unapproved articles'),
    url(r'^(?P<article_id>[0-9]+)/approve$', views.approve_article, name='approve article'),
    url(r'^(?P<article_id>[0-9]+)/unapprove$', views.unapprove_article, name='unapproves article'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.articles_by_tag, name='articles by tag'),
    url(r'^user/$', views.articles_by_user, name='articles by user'),
    url(r'^(?P<article_id>[0-9]+)/delete/$', views.delete_article, name='delete article'),

]
