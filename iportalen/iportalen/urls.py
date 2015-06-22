from django.conf.urls import include, url
from django.contrib import admin
from iportalen import articles

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/$', ),
]
