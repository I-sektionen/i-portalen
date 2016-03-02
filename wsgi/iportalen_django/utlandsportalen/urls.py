from django.conf.urls import url, include
from . import views


app_name = 'utlandsportalen'

utlandsportalen_patterns = [
    url(r'^$',             view=views.show_utlandsportalen,      name="show_utlandsportalen"),
    url(r'^blogs/$',         view=views.show_blogs,                name="utl_blogs"),
    url(r'^contact/$',       view=views.show_contact,              name="utl_contact"),
    url(r'scholarships/$',  view=views.show_scholarships,         name="utl_scholarships"),
]

urlpatterns = [url(r'^', include(utlandsportalen_patterns, namespace=app_name))]