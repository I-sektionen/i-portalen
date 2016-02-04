from django.conf.urls import include, url
from utils.admin import iportalen_admin_site
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemaps import (
    StaticViewSitemapHigh,
    EventSitemap,
    ArticleSitemap,
    StaticViewSitemapLow,
    OrganisationSitemap,
    StaticViewSitemapMedium
)

sitemaps = {
    'static': StaticViewSitemapHigh,
    'event': EventSitemap,
    'article': ArticleSitemap,
    'organisations': OrganisationSitemap,
    'static_low': StaticViewSitemapLow,
    'static_mid': StaticViewSitemapMedium,
}

urlpatterns = [
    url(r'^$',             view=views.display_news_feed,         name="news feed"),
    url(r'^sponsored/$',   view=views.display_sponsored_content, name="sponsored"),
    url(r'^placeholder/',  view=views.placeholder,               name="placeholder"),
    url(r'^file_storage/', view=views.glasscubes_link,           name="glasscubes storage"),

    url(r'^admin/',             include(iportalen_admin_site.urls)),
    url(r'^article/',           include('articles.urls')),
    url(r'^booking/',           include('bookings.urls')),
    url(r'^course_evaluation/', include('course_evaluations.urls')),
    url(r'^event/',             include('events.urls')),
    url(r'^faq/',               include('faq.urls')),
    url(r'^organisations/',     include('organisations.urls')),
    url(r'^user/',              include('user_managements.urls')),
    url(r'^voting/',            include('votings.urls')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(r'^pul/$',       view=TemplateView.as_view(template_name="pul.html"), name="pul"),
    url(r'^cookies/$',   view=TemplateView.as_view(template_name="cookies.html"), name="cookies"),
    url(r'^robots.txt$', view=TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    url(r'^.well-known/acme-challenge/o1RETI1T86n55DRPYdvyBNK5C5mzfvWk33Mhz5CyT_8',
        view=TemplateView.as_view(template_name='acme.txt', content_type='text/plain')),

    # Om någon har sparat /student som favorit skickar vi dem till startsidan
    url(r'^student', RedirectView.as_view(pattern_name='front page', permanent=True)),
]
if not settings.ON_PASS:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
