from django.conf.urls import url

from .views import (
    view_event,
    register_to_event,
    create_or_modify_event,
    administer_event,
    preregistrations_list,
    participants_list,
    check_in,
    all_unapproved_events,
    approve_event,
    unapprove_event,
    register_as_reserve,
    CSV_view_participants,
    CSV_view_preregistrations,
    unregister,
    event_calender,
    event_calender_view,
    reserves_list,
    registered_on_events,
    events_by_user,
    speech_nr_list,
    speaker_list,
    speaker_list_display,
    administer_speaker_list,
    import_registrations,
    file_download,
    calendar_feed,
    personal_calendar_feed,
    summarise_noshow,
    speaker_list_user_add_self,
    user_view,
    speaker_list_user_remove_self,
    upload_attachments_images,
    upload_attachments,
    download_attachment,)

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', view=view_event, name="event"),
    url(r'^create/$', view=create_or_modify_event, name="create"),
    url(r'^(?P<pk>[0-9]+)/edit/$', view=create_or_modify_event, name="edit"),
    url(r'^(?P<pk>[0-9]+)/register/$', view=register_to_event, name="register to"),
    url(r'^(?P<pk>[0-9]+)/register_reserve/$', view=register_as_reserve, name="register as reserve"),
    url(r'^(?P<pk>[0-9]+)/unregister/$', view=unregister, name="unregister"),
    url(r'^(?P<pk>[0-9]+)/administer/$', view=administer_event, name="administer event"),
    url(r'^(?P<pk>[0-9]+)/administer/preregistrations/$', view=preregistrations_list, name="preregistrations"),
    url(r'^(?P<pk>[0-9]+)/administer/participants/$', view=participants_list, name="participants"),
    url(r'^(?P<pk>[0-9]+)/administer/import_preregistrations/$', view=import_registrations, name="import registrations"),
    url(r'^(?P<pk>[0-9]+)/administer/speech_nr_list/$', view=speech_nr_list, name="speech nr list"),
    url(r'^(?P<pk>[0-9]+)/user_add_self_speech_list/$', view=speaker_list_user_add_self, name="add user speech nr list"),
    url(r'^(?P<pk>[0-9]+)/user_remove_self_speech_list/$', view=speaker_list_user_remove_self, name="remove user speech nr list"),
    url(r'^(?P<pk>[0-9]+)/user_view/$', view=user_view, name="user view"),
    url(r'^(?P<pk>[0-9]+)/administer/reserves/$', view=reserves_list, name="reserves"),
    url(r'^(?P<pk>[0-9]+)/administer/participants/download/$', view=CSV_view_participants,
        name="participants download"),
    url(r'^(?P<pk>[0-9]+)/administer/preregistrations/download/$', view=CSV_view_preregistrations,
        name="preregistrations download"),
    url(r'^(?P<pk>[0-9]+)/administer/event_check_in/$', view=check_in, name="check in"),
    url(r'^(?P<pk>[0-9]+)/administer/noshow/$', view=summarise_noshow, name="no show"),
    url(r'^unapproved/$', view=all_unapproved_events, name='unapproved'),
    url(r'^(?P<event_id>[0-9]+)/approve$', view=approve_event, name='approve'),
    url(r'^(?P<pk>[0-9]+)/unapprove$', view=unapprove_event, name='unapprove'),
    url(r'^calendar/$', view=event_calender, name='calender'),
    url(r'^calendar_view/$', view=event_calender_view, name='calender_view'),
    url(r'^user_entries/$', view=registered_on_events, name='registered on'),
    url(r'^my_events/$', view=events_by_user, name='by user'),
    url(r'^(?P<pk>[0-9]+)/administer/speaker/$', view=administer_speaker_list, name="administer speaker list"),
    url(r'^(?P<pk>[0-9]+)/administer/speaker/display/$', view=speaker_list_display, name="speaker display"),
    url(r'^(?P<pk>[0-9]+)/administer/speaker/api/$', view=speaker_list, name="speaker api"),
    url(r'^(?P<pk>[0-9]+)/download/$', view=file_download, name='download'),
    url(r'^feed/feed.ics$', view=calendar_feed, name='calendar feed'),
    url(r'^feed/(?P<liu_id>[a-z]{4,5}\d{3})/feed.ics$', view=personal_calendar_feed, name='personal calendar feed'),
    url(r'^(?P<pk>[0-9]+)/attachments/$', upload_attachments, name='manage attachments'),
    url(r'^(?P<pk>[0-9]+)/images/$', upload_attachments_images, name='manage images'),
    url(r'^attachments/other/(?P<pk>[0-9]+)/$', download_attachment, name='download attachment')
]
