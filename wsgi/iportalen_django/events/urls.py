from django.conf.urls import url
from .views import (
    view_event,
    register_to_event,
    create_event,
    administer_event,
    participants_list,
    check_in,
    all_unapproved_events,
    approve_event,
    unapprove_event,
)

urlpatterns = [
    url(r'(?P<pk>[0-9]+)/$', view=view_event, name="event"),
    url(r'create_event/$', view=create_event, name="create event"),
    url(r'(?P<pk>[0-9]+)/register/$', view=register_to_event, name="register_to_event"),
    url(r'(?P<pk>[0-9]+)/administer/$', view=administer_event, name="administer_event"),
    url(r'(?P<pk>[0-9]+)/administer/participants/$', view=participants_list, name="event_participants"),
    url(r'(?P<pk>[0-9]+)/administer/checkin/$', view=check_in, name="check in"),
    url(r'^unapproved/$', view=all_unapproved_events, name='unapproved events'),
    url(r'^(?P<event_id>[0-9]+)/approve$', view=approve_event, name='approve event'),
    url(r'^(?P<event_id>[0-9]+)/unapprove$', view=unapprove_event, name='unapprove event'),
]
