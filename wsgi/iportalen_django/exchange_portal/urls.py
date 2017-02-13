from django.conf.urls import url, include
from . import views

app_name = 'exchange_portal'


exchange_portal_patterns = [
    url(r'^$',                           view=views.Exchange_Portal,          name="exchange_portal"),
    url(r'^search/$',                    view=views.Search,                   name='search'),
    url(r'^school/(?P<pk>[0-9]+)/$',     view=views.Exchange_School,          name='school'),
    url(r'^search-autocomplete/$', view=views.Search_Autocomplete.as_view(),  name='search_autocomplete'),

]


urlpatterns = [url(r'^', include(exchange_portal_patterns, namespace=app_name))]