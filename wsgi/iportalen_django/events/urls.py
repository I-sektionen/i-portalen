from django.conf.urls import url, include
from . import views

app_name = 'events'


admin_patterns = [
    url(r'^$',                           view=views.administer_event,          name="administer event"),
    url(r'^preregistrations/$',          view=views.preregistrations_list,     name="preregistrations"),
    url(r'^participants/$',              view=views.participants_list,         name="participants"),
    url(r'^import_preregistrations/$',   view=views.import_registrations,      name="import registrations"),
    url(r'^speech_nr_list/$',            view=views.speech_nr_list,            name="speech nr list"),
    url(r'^reserves/$',                  view=views.reserves_list,             name="reserves"),
    url(r'^participants/download/$',     view=views.CSV_view_participants,     name="participants download"),
    url(r'^preregistrations/download/$', view=views.CSV_view_preregistrations, name="preregistrations download"),
    url(r'^event_check_in/$',            view=views.check_in,                  name="check in"),
    url(r'^noshow/$',                    view=views.summarise_noshow,          name="no show"),
]

event_patterns = [
    url(r'^(?P<pk>[0-9]+)/$',                  view=views.view_event,             name="event"),
    url(r'create/$',                           view=views.create_or_modify_event, name="create"),
    url(r'^(?P<pk>[0-9]+)/edit/$',             view=views.create_or_modify_event, name="edit"),
    url(r'^(?P<pk>[0-9]+)/register/$',         view=views.register_to_event,      name="register to"),
    url(r'^(?P<pk>[0-9]+)/register_reserve/$', view=views.register_as_reserve,    name="register as reserve"),
    url(r'^(?P<pk>[0-9]+)/unregister/$',       view=views.unregister,             name="unregister"),
    url(r'^unapproved/$',                      view=views.all_unapproved_events,  name='unapproved'),
    url(r'^(?P<event_id>[0-9]+)/approve$',     view=views.approve_event,          name='approve'),
    url(r'^(?P<pk>[0-9]+)/unapprove$',         view=views.unapprove_event,        name='unapprove'),
    url(r'^calendar/$',                        view=views.event_calender,         name='calender'),
    url(r'^calendar_view/$',                   view=views.event_calender_view,    name='calender_view'),
    url(r'^user_entries/$',                    view=views.registered_on_events,   name='registered on'),
    url(r'^my_events/$',                       view=views.events_by_user,         name='by user'),
    url(r'^feed/feed.ics$',                    view=views.calendar_feed,          name='calendar feed'),
    url(r'^feed/(?P<liu_id>[a-z]{4,5}\d{3})/feed.ics$',
        view=views.personal_calendar_feed, name='personal calendar feed'),
    url(r'^(?P<pk>[0-9]+)/user_view/$',        view=views.user_view,              name="user view"),
    url(r'^(?P<pk>[0-9]+)/attachments/$',      view=views.upload_attachments,     name='manage attachments'),
    url(r'^(?P<pk>[0-9]+)/images/$',           view=views.upload_attachments_images, name='manage images'),
    url(r'^no_shows/$',                        view=views.show_noshows,           name="no_shows"),
    url(r'^(?P<pk>[0-9]+)/administer/', include(admin_patterns)),
    url(r'^no_shows/remove$',                  view=views.remove_noshow,          name="remove_noshow"),
    url(r'^(?P<pk>[0-9]+)/cancel/$',           view=views.cancel,                 name="cancel"),
    url(r'^(?P<pk>[0-9]+)/confirm_cancel/$',   view=views.confirm_cancel,         name="confirm_cancel"),
]

urlpatterns = [url(r'^', include(event_patterns, namespace=app_name))]