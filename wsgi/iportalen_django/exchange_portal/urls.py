from django.conf.urls import url, include
from . import views

app_name = 'exchange_portal'


exchange_portal_patterns = [
    url(r'^$',                           view=views.Exchange_Portal,          name="exchange_portal"),
    url(r'^important_dates/$',           view=views.Important_Dates,          name='important_dates'),
    url(r'^contact/$',                   view=views.Contact,                  name='contact'),
    url(r'^add_country/$',                   view=views.Add_Country,            name='add_country'),
    url(r'^add_city/$',                   view=views.Add_City,                  name='add_city'),
    url(r'^add_school/$',                   view=views.Add_School,              name='add_school'),
    url(r'^add_liu_course/$',                   view=views.Add_Liu_Course,      name='add_liu_course'),
    url(r'^add_exchange_course/$',                   view=views.Add_Exchange_Course,
        name='add_exchange_course'),
    url(r'^school/(?P<pk>[0-9]+)/$',     view=views.Exchange_School,          name='school'),
    url(r'^search-autocomplete/$', view=views.Search_Autocomplete.as_view(),  name='search_autocomplete'),
    url(r'^travel_stories/$',   view=views.Travel_Stories,    name="travel_stories"),
    url(r'^asia/$',   view=views.Asia,    name="asia"),
    url(r'^asia/(?P<filter>\w{0,50})/$',   view=views.Asia_filtered,    name="asia"),

]


urlpatterns = [url(r'^', include(exchange_portal_patterns, namespace=app_name))]
