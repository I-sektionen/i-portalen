from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.all_articles, name='articles'),
    url(r'^(?P<pk>[0-9]+)/$', views.single_article, name='article'),
    url(r'^create/$', views.create_or_modify_article, name='create'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.create_or_modify_article, name='edit'),
    url(r'^unapproved/$', views.all_unapproved_articles, name='unapproved'),
    url(r'^(?P<pk>[0-9]+)/approve$', views.approve_article, name='approve'),
    url(r'^(?P<pk>[0-9]+)/unapprove$', views.unapprove_article, name='unapproves'),
    url(r'^tag/(?P<tag_name>[^/]+)/$', views.articles_by_tag, name='by tag'),
    url(r'^my_articles/$', views.articles_by_user, name='by user'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete_article, name='delete'),
    url(r'^(?P<pk>[0-9]+)/download/$', views.article_file_download, name='download'),
    url(r'^(?P<article_pk>[0-9]+)/attachments/$', views.upload_attachments, name='manage attachments'),
    url(r'^(?P<article_pk>[0-9]+)/images/$', views.upload_attachments_images, name='manage images'),
    url(r'^attachments/other/(?P<pk>[0-9]+)/$', views.download_attachment, name='download attachment')

]
