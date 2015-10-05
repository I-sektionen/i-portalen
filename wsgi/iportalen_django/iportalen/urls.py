from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from .views import create_content

from articles import urls as article_urls
from user_managements import urls as user_urls
from events import urls as event_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="front page")),
    url(r'^articles/', include(article_urls)),
    url(r'^user/', include(user_urls)),
    url(r'event/', include(event_urls)),
    url(r'create_content', view=create_content, name="create content")
]
