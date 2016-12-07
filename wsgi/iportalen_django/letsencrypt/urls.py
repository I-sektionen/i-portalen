from django.conf.urls import url, include
from . import views

app_name = 'letsencrypt'


letsencrypt_patterns = [
    url(r'^(?P<url>[^/]+)$', view=views.verification,   name="verify domain"),
]

urlpatterns = [url(r'^', include(letsencrypt_patterns, namespace=app_name))]