from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class EventManager(models.Manager):
    def published(self):
        return self.filter(
                status=self.model.APPROVED,
                visible_from__lte=timezone.now(),
                end__gte=timezone.now()
                ).order_by('-start')


class SpeakerListManager(models.Manager):
    @staticmethod
    def get_first(event):
        try:
            return event.speakerlist_set.get(first=True, event=event)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_last(event):
        try:
            q = event.speakerlist_set.get(next_speaker=None, event=event)
            return q
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all(event):
        try:
            return event.speakerlist_set.all()
        except ObjectDoesNotExist:
            return None
