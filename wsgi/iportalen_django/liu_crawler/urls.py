from django.conf.urls import url, include
from . import views

app_name = "liu_crawler"

liu_crawler_patterns = [
    url(r'^$',                                         view=views.liu_crawler,       name='liu_crawler'),
    url(r'^add/$', view=views.add_result,   name="add_result"),
    url(r'^get/$', view=views.get_result,   name="get_result"),
]

urlpatterns = [url(r'^', include(liu_crawler_patterns, namespace=app_name))]
