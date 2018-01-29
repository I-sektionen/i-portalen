from django.conf.urls import url, include
from . import views

app_name = 'alumni_portal'


alumni_patterns = [
    url(r'^$', view=views.alumni_portal, name='alumni_portal')
]

urlpatterns = [url(r'^', include(alumni_patterns, namespace=app_name))]
