from django.contrib import sitemaps
from django.core.urlresolvers import reverse

from events.models import Event
from articles.models import Article


class StaticViewSitemapLow(sitemaps.Sitemap):
    priority = 0.2
    changefreq = 'weekly'

    def items(self):
        return ['pul']  # Add static url names here (that should be indexed by search engines)!

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