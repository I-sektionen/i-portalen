from django.conf.urls import url, include
from . import views

app_name = 'webgroup'


webgroup_patterns = [
    url(r'^$',                   view=views.landing,                 name="landing"),
    url(r'^github/$',            view=views.github_stats,            name="github"),
    url(r'^kurser/$',            view=views.exam_statistics,         name="exam_statistics"),
    url(r'^kurser/grupper/$',    view=views.exam_statistics_groups,  name="exam_statistics_groups"),
    url(r'^kurser/update$',      view=views.exam_statistics_update,  name="exam_statistics_update"),
]

urlpatterns = [url(r'^', include(webgroup_patterns, namespace=app_name))]