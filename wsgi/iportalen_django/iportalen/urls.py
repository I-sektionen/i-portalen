from django.conf.urls import include, url
from django.contrib import admin
from combined_views import views as combined_views_view
from articles import urls as article_urls
from bookings import urls as booking_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', combined_views_view.index, name='index'),
    url(r'^articles/', include(article_urls)),
    url(r'^booking/', include(booking_urls))
]
