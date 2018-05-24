from django.conf.urls import url, include
from . import views

app_name = 'exchange_portal'


exchange_portal_patterns = [
    url(r'^$',                           view=views.Exchange_Portal,          name="exchange_portal"),
    url(r'^admin/$',                           view=views.Admin,            name="admin"),
    url(r'^feedback/$',                           view=views.Add_Feedback,            name="feedback"),
    url(r'^important_dates/$',           view=views.Important_Dates,          name='important_dates'),
    url(r'^contact/$',                   view=views.Contact,                  name='contact'),
    url(r'^school/(?P<pk>[0-9]+)/$',     view=views.Exchange_School,          name='school'),
    url(r'^search-autocomplete/$', view=views.Search_Autocomplete.as_view(),  name='search_autocomplete'),
    url(r'^travel_stories/$',   view=views.Travel_Stories,    name="travel_stories"),
    url(r'^travel_story/(?P<pk>[0-9]+)/$', view=views.single_travel_story, name='travel_story'),
    url(r'^(?P<continent>\w{0,50})/$',   view=views.continent,    name="continent"),
    url(r'asien/(?P<country>\w{0,50})$',   view=views.continent_filtered,    name="country"),
    url(r'nordamerika/(?P<country>\w{0,50})$',   view=views.continent_filtered,    name="country"),
    url(r'europa/(?P<country>\w{0,50})$',   view=views.continent_filtered,    name="country"),
    url(r'afrika/(?P<country>\w{0,50})$',   view=views.continent_filtered,    name="country"),
    url(r'oceanien/(?P<country>\w{0,50})$',   view=views.continent_filtered,    name="country"),
    url(r'sydamerika/(?P<country>\w{0,50})$',   view=views.continent_filtered,    name="country")

]


urlpatterns = [url(r'^', include(exchange_portal_patterns, namespace=app_name))]
