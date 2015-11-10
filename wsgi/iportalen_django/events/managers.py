from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class SpeakerListManager(models.Manager):

    def get_first(self, event):
        try:
            return event.speakerlist_set.get(first=True, event=event)
        except ObjectDoesNotExist:
            return None

    def get_last(self, event):
        try:
            q = event.speakerlist_set.get(next_speaker=None, event=event)
            return q
        except ObjectDoesNotExist:
            return None

    def get_all(self, event):
        try:
            return event.speakerlist_set.all()
        except ObjectDoesNotExist:
            return None