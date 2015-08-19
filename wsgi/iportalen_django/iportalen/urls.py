from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from articles import urls as article_urls
from bookings import urls as booking_urls



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="front_page.html")),
    url(r'^articles/', include(article_urls)),
    url(r'^booking/', include(booking_urls))
]
