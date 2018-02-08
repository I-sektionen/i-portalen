from django.conf.urls import url, include
from . import views

app_name = 'webgroup'


webgroup_patterns = [
    url(r'^$',                   view=views.landing,                 name="landing"),
    url(r'^github/$',            view=views.github_stats,            name="github"),

]

urlpatterns = [url(r'^', include(webgroup_patterns, namespace=app_name))]