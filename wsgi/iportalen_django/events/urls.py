from django.conf.urls import url
from .views import event, register_to_event, create_event

urlpatterns = [
    url(r'(?P<pk>[0-9]+)/$', view=event, name="event"),
    url(r'create_event/$', view=create_event, name="create event"),
    url(r'(?P<pk>[0-9]+)/register', view=register_to_event, name="register_to_event"),
]
