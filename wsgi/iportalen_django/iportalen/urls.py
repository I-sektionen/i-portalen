from django.conf.urls import include, url

from utils.admin import iportalen_admin_site, iportalen_superadmin_site
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
    url(r'^$',             view=views.landing,                   name="news feed"),
    url(r'^news_api$',     view=views.news_content,              name="news api"),
    url(r'^sponsored/$',   view=views.display_sponsored_content, name="sponsored"),
    url(r'^job_adverts/$', view=views.display_job_advert_content,name="job_adverts"),
    url(r'^placeholder/',  view=views.placeholder,               name="placeholder"),
    url(r'^file_storage/$',view=views.glasscubes_link,           name="glasscubes storage"),

    url(r'^file_storage/course_evaluations$', view=views.glasscubes_link_course, name="glasscubes storage course"),
    url(r'^file_storage/i-bibles$',           view=views.glasscubes_link_bible, name="glasscubes storage bible"),

    url(r'^admin/',             include(iportalen_admin_site.urls)),
    url(r'^superadmin/',        include(iportalen_superadmin_site.urls)),
    #Pattern matching in URL since APPEND_SLASH in settings doesnt work
    url(r'^alumni_portal/?',    include('alumni_portal.urls')),
    url(r'^article/',           include('articles.urls')),
    url(r'^booking/',           include('bookings.urls')),
    url(r'^course_evaluation/', include('course_evaluations.urls')),
    url(r'^event/',             include('events.urls')),
    url(r'^faq/',               include('faq.urls')),
    url(r'^organisations/',     include('organisations.urls')),
    url(r'^user/',              include('user_managements.urls')),
    url(r'^voting/',            include('votings.urls')),
    url(r'^speaker/',           include('speaker_list.urls')),
    url(r'^fika_penalty/',      include('fika_penalty.urls')),
    url(r'^exchange_portal/',   include('exchange_portal.urls')),
    url(r'^liu-crawler/',       include('liu_crawler.urls')),
    url(r'^webgroup/',          include('webgroup.urls')),
    url(r'^exjobbsportalen/',   include('thesis_portal.urls')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(r'^gdpr/$',      view=TemplateView.as_view(template_name="gdpr.html"), name="gdpr"),
    url(r'^cookies/$',   view=TemplateView.as_view(template_name="cookies.html"), name="cookies"),
    url(r'^robots.txt$', view=TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    url(r'^.well-known/acme-challenge/', include('letsencrypt.urls')),

    # Om någon har sparat /student som favorit skickar vi dem till startsidan
    url(r'^student', RedirectView.as_view(pattern_name='news feed', permanent=True)),
    url(r'^soekande', view=views.isektionen_link),
    url(r'^foeretag', view=views.isektionen_link),
    url(r'^alumn', RedirectView.as_view(pattern_name='news feed', permanent=True)),
    url(r'^utlandsportalen', RedirectView.as_view(pattern_name='news feed', permanent=True)),
    url(r'^i-profilen', RedirectView.as_view(pattern_name='user_management:my page', permanent=True)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include("user_managements.api_urls")),

]
if not (settings.ON_PASS or settings.ON_AWS):
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
