from django.conf.urls import include, url
from django.contrib import admin
from utils.admin import iportalen_admin_site
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap


from .views import placeholder, display_news_feed, glasscubes_link, display_sponsored_content

from articles import urls as article_urls
from user_managements import urls as user_urls
from events import urls as event_urls
from organisations import urls as org_urls
from bookings import urls as booking_urls
from course_evaluations import urls as course_urls
from .sitemaps import StaticViewSitemapHigh, EventSitemap, ArticleSitemap, StaticViewSitemapLow

sitemaps = {
    'static': StaticViewSitemapHigh,
    'event': EventSitemap,
    'article': ArticleSitemap,
    'static_low': StaticViewSitemapLow
}

urlpatterns = [
    url(r'^admin/', include(iportalen_admin_site.urls)),
    url(r'^$', view=display_news_feed, name="news feed"),
    url(r'^sponsored/$', view=display_sponsored_content, name="sponsored"),
    url(r'^article/', include(article_urls, namespace="articles")),
    url(r'^user/', include(user_urls)),
    url(r'^event/', include(event_urls, namespace="events")),
    url(r'^organisations/', include(org_urls, namespace="organisations")),
    url(r'^booking/', include(booking_urls, namespace="bookings")),
    url(r'^placeholder/', view=placeholder, name="placeholder"),
    url(r'^student', RedirectView.as_view(pattern_name='front page', permanent=True)),  # Om någon har sparat /student som favorit skickar vi dem till startsidan
    url(r'^course_evaluation/', include(course_urls, namespace="course_evaluations")),
    url(r'^file_storage/', view=glasscubes_link, name="glasscubes storage"),
    url(r'^faq/', include('faq.urls', namespace="faq")),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'.well-known/acme-challenge/o1RETI1T86n55DRPYdvyBNK5C5mzfvWk33Mhz5CyT_8', TemplateView.as_view(template_name='acme.txt', content_type='text/plain')),
    url(r'pul/$', view=TemplateView.as_view(template_name="pul.html"), name="pul"),
    url(r'cookies/$', view=TemplateView.as_view(template_name="cookies.html"), name="cookies")
]
if not settings.ON_PASS:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
