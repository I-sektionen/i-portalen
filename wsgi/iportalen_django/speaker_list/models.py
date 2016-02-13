from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from events.models import Event
from iportalen import settings
from speaker_list.managers import SpeakerListManager
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


class SpeakerList(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("arrangemang"), null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("användare"), null=True, on_delete=models.SET_NULL)
    first = models.NullBooleanField(default=None)
    next_speaker = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_NULL)

    objects = SpeakerListManager()

    def move_up(self):
        if self.first:
            return
        # Find event above and switch order
        above = SpeakerList.objects.get(next_speaker=self)
        above.next_speaker = self.next_speaker
        self.next_speaker = above
        if above.first:
            self.first = True
            above.first = False
        self.save()
        above.save()

    def move_down(self):
        if self.next_speaker is None:
            return
        below = self.next_speaker
        if self.first:
            if below is None:
                return
            self.next_speaker = below.next_speaker
            below.next_speaker = self
            below.first = True
        else:
            above = SpeakerList.object.get(next_speaker=self)
            above.next_speaker = below
            self.next_speaker = below.next_speaker
            below.next_speaker = self
            above.save()
        self.save()
        below.save()

    def __str__(self):
        return str(self.event) + " | " + str(self.user)

    def get_user_from_speech_nr(self, event, speech_nr):
        return event.entryasparticipant_set.get(speech_nr=speech_nr)

    def get_speech_num_from_user(self, event, user):
        return event.entryasparticipant_set.get(user=user).speech_nr

    def add_speaker_to_queue(self, event, speech_nr):
        u = event.get_user_from_speech_nr(speech_nr=speech_nr).user
        first_object = not SpeakerList.objects.filter(event=event).exists()
        if not first_object:
            last = SpeakerList.objects.get(event=event, next_speaker=None)
            s = SpeakerList.objects.create(user=u, event=event)
            s.first = False
            last.next_speaker = s
            last.save()
        else:
            s = SpeakerList.objects.create(user=u, event=event)
            s.first = True
        s.save()
        return True

    def clear_speaker_queue(self, event):
        q = SpeakerList.objects.filter(event=event)
        for element in q:
            element.delete()

    def remove_first_speaker_from_queue(self, event):
        sp = SpeakerList.objects.get_first(event=event)
        if sp.next_speaker is not None:
            sp.next_speaker.first = True
            sp.next_speaker.save()
        sp.delete()

    def remove_speaker_from_queue(self, event, speech_nr):
        u = event.get_user_from_speech_nr(speech_nr=speech_nr).user
        to_remove = SpeakerList.objects.filter(event=event, user=u)
        for ele in to_remove:
            event._remove_speaker_from_queue(ele)

    @staticmethod
    def _remove_speaker_from_queue(to_remove):
        before = None
        after = None
        try:
            before = SpeakerList.objects.get(next_speaker=to_remove)
        except ObjectDoesNotExist:
            pass
        try:
            after = to_remove.next_speaker
        except ObjectDoesNotExist:
            pass
        if (before is None) and (after is not None):
            # First element of several
            after.first = True
            after.save()
        elif (before is not None) and (after is not None):
            # Middle element
            before.next_speaker = after
            before.save()
        # Case: Single element, last element.
        to_remove.delete()

    def get_speaker_queue(self, event):
        try:
            first = SpeakerList.objects.get(event=event, first=True)
        except ObjectDoesNotExist:
            return []

        result = [{'first_name': first.user.first_name,
                   'last_name': first.user.last_name,
                   'speech_nr': first.user.entryasparticipant_set.get(event=event).speech_nr}]
        next_speaker = first.next_speaker
        while next_speaker is not None:
            result.append({'first_name': next_speaker.user.first_name,
                           'last_name': next_speaker.user.last_name,
                           'speech_nr': next_speaker.user.entryasparticipant_set.get(event=event).speech_nr})
            next_speaker = next_speaker.next_speaker
        return result