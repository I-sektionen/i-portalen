import random

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from .exceptions import SpeakerListException


class SpeakerListManager(models.Manager):

    def clear(self, event):
        self.filter(event=event).delete()

    @transaction.atomic
    def add(self, event, user):
        if not event.is_checked_in(user):
            raise SpeakerListException(reason=_('Ej incheckad.'))
        if self.filter(event=event, user=user, has_spoken=False).count() == 0:  # don't add if already on list
            try:
                speech_id = self.filter(event=event).order_by('-speech_id')[0].speech_id + 1
            except IndexError:
                speech_id = 1
            if self.filter(event=event, has_spoken=False).count() == 0:
                nr_of_speeches = 0
            else:
                nr_of_speeches = self.filter(event=event, user=user, has_spoken=True).count() + 1
            self.create(event=event, user=user, nr_of_speeches=nr_of_speeches, has_spoken=False, speech_id=speech_id)
        else:
            raise SpeakerListException(reason=_('Finns redan på listan.'))

    def show_queue(self, event):
        speaker_list = self.filter(event=event, has_spoken=False)
        result = []
        for l in speaker_list:
            result.append({'first_name': l.user.first_name,
                           'last_name': l.user.last_name,
                           'speech_nr': l.user.entryasparticipant_set.get(event=event).speech_nr})
        return result

    @transaction.atomic
    def next(self, event):
        try:
            speakers = self.filter(event=event, has_spoken=False)
            speaker = speakers[0]
            try:
                next_speaker = speakers[1]
                next_speaker.nr_of_speeches = 0
                next_speaker.save()
            except IndexError:
                # No next speaker
                pass
            speaker.has_spoken = True
            speaker.save()
        except:
            raise SpeakerListException(reason=_('Listan är tom'))

    def remove(self, event, user):
        try:
            speaker = self.get(event=event, has_spoken=False, user=user)
            if speaker.nr_of_speeches == 0:
                raise SpeakerListException(reason=_('Du kan inte stryka dig om du är högst upp på talarlistan.'))
            speaker.delete()
        except SpeakerListException as e:
            raise e
        except:
            raise SpeakerListException(reason=_('Listan är tom'))

    @transaction.atomic
    def shuffle(self, event):
        self.next(event)
        speakers = self.filter(event=event, has_spoken=False).order_by('speech_id')
        nr_of_speakers = ((speakers.count() * -1) - abs(speakers[0].speech_id) - 1)
        speakers = sorted(list(speakers), key=lambda x: random.random())
        for speaker in speakers:
            speaker.nr_of_speeches = 1
            speaker.speech_id = nr_of_speakers
            speaker.save()
            nr_of_speakers += 1
