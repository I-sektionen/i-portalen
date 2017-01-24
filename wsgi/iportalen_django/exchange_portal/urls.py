from django.conf.urls import url, include
from . import views

app_name = 'exchange_portal'


exchange_portal_patterns = [
    url(r'^$',                           view=views.Exchange_Portal,          name="exchange_portal"),
    url(r'^search/$',                    view=views.Search,          name='search'),
    url(r'^travel_story/$',              view=views.View_Story,             name="travel_story"),
]


urlpatterns = [url(r'^', include(exchange_portal_patterns, namespace=app_name))]