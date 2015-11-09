from django.db import models


class SpeakerListManager(models.Manager):

    def get_first(self, event):
        return event.speakerlist_set.get(first=True)

    def get_last(self, event):
        return event.speakerlist_set.get(next_speaker=None)

    def get_all(self, event):
        return event.speakerlist_set

