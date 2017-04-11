from django.conf.urls import url, include
from . import views

app_name = 'webgroup'


webgroup_patterns = [
    url(r'$',                   view=views.landing,   name="landing"),
]

urlpatterns = [url(r'^', include(webgroup_patterns, namespace=app_name))]