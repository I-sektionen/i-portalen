from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from django.db.models import Q

from events.models import Event
from articles.models import Article
from organisations.models import Organisation


class StaticViewSitemapLow(sitemaps.Sitemap):
    priority = 0.2
    changefreq = 'yearly'

    def items(self):
        return ['pul', 'cookies']  # Add static url names here (that should be indexed by search engines)!

    def location(self, obj):
        return reverse(obj)


class StaticViewSitemapMedium(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['faq:faq_topic_list', 'course_evaluations:evaluate course']

    def location(self, obj):
        return reverse(obj)


class StaticViewSitemapHigh(sitemaps.Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return ['news feed', 'events:calender']  # Add static url names here (that should be indexed by search engines)!

    def location(self, obj):
        return reverse(obj)


class EventSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return Event.objects.published()

    def lastmod(self, obj):
        return obj.modified


class ArticleSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return Article.objects.published()

    def lastmod(self, obj):
        return obj.modified


class OrganisationSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return Organisation.objects.filter(Q(organisation_type=Organisation.SEKTIONEN) |
                                           Q(organisation_type=Organisation.FORENINGAR))
