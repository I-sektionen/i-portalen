from django.conf.urls import include, url
from django.contrib import admin
from articles import urls as article_urls
from user_managements import urls as user_urls
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="front_page.html")),
    url(r'^articles/', include(article_urls)),
    url(r'^user/', include(user_urls)),
]
