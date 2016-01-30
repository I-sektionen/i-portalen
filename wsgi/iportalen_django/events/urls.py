from django.conf.urls import url, include
from . import views

app_name = 'events'


admin_patterns = [
    url(r'^$',                           view=views.administer_event,          name="administer event"),
    url(r'^speaker/$',                   view=views.administer_speaker_list,   name="administer speaker list"),
    url(r'^speaker/display/$',           view=views.speaker_list_display,      name="speaker display"),
    url(r'^speaker/api/$',               view=views.speaker_list,              name="speaker api"),
    url(r'^preregistrations/$',          view=views.preregistrations_list,     name="preregistrations"),
    url(r'^participants/$',              view=views.participants_list,         name="participants"),
    url(r'^import_preregistrations/$',   view=views.import_registrations,      name="import registrations"),
    url(r'^speech_nr_list/$',            view=views.speech_nr_list,            name="speech nr list"),
    url(r'^reserves/$',                  view=views.reserves_list,             name="reserves"),
    url(r'^participants/download/$',     view=views.CSV_view_participants,     name="participants download"),
    url(r'^preregistrations/download/$', view=views.CSV_view_preregistrations, name="preregistrations download"),
    url(r'^event_check_in/$',            view=views.check_in,                  name="check in"),
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
    url(r'^(?P<pk>[0-9]+)/download/$',         view=views.file_download,          name='download'),
    url(r'^feed/$',                            view=views.calendar_feed,          name='calendar feed'),
    url(r'^feed/feed.ics$',                    view=views.calendar_feed,          name='calendar feed'),

    url(r'^(?P<pk>[0-9]+)/administer/', include(admin_patterns)),

]

urlpatterns = [url(r'^', include(event_patterns, namespace=app_name))]