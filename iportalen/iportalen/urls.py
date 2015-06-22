from django.conf.urls import include, url
from django.contrib import admin
from front_page import views as front_page_view
from articles import urls as article_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', front_page_view.index, name='index'),
    url(r'^articles/', include(article_urls)),
]
