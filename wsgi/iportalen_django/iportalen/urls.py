from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .views import create_content, approve_content, placeholder

from articles import urls as article_urls
from user_managements import urls as user_urls
from events import urls as event_urls
from organisations import urls as org_urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="front_page.html"), name="front page"),
    url(r'^articles/', include(article_urls)),
    url(r'^user/', include(user_urls)),
    url(r'^event/', include(event_urls)),
    url(r'^create_content/', view=create_content, name="create content"),
    url(r'^approve_content/', view=approve_content, name="approve content"),
    url(r'^organisations/', include(org_urls)),
    url(r'^placeholder/', view=placeholder, name="placeholder"),
    url(r'^student', RedirectView.as_view(pattern_name='front page')),  # Om någon har sparat /student som favorit skickar vi dem till startsidan
]
if not settings.ON_PASS:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
