from django.conf.urls import url
from .views import event, register_to_event

urlpatterns = [
    url(r'(?P<pk>[0-9]+)/$', view=event, name="event"),
    url(r'(?P<pk>[0-9]+)/register', view=register_to_event, name="register_to_event")
]