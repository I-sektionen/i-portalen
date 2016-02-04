from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from utils.time import six_months_back


class EventManager(models.Manager):
    def published(self):
        return self.filter(
                status=self.model.APPROVED,
                visible_from__lte=timezone.now(),
                end__gte=timezone.now()
                ).order_by('-start')

    def events_by_user(self, user):
        """Returns the events a specific user is preregistered to.
        :param user: A django user.
        """
        r = self.filter(entryaspreregistered__user=user)
        return r


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


class EntryAsPreRegisteredManager(models.Manager):
    def get_noshow(self, user):
        return self.filter(user=user, no_show=True, timestamp__gte=six_months_back)


