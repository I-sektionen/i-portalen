from django.db import models
from events.models import Event
from iportalen import settings
from speaker_list.managers import SpeakerListManager
from django.utils.translation import ugettext_lazy as _


class SpeakerList(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("arrangemang"), null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("användare"), null=True, on_delete=models.SET_NULL)
    speech_id = models.IntegerField(default=1, verbose_name=_("talar id"), unique=True)
    nr_of_speeches = models.IntegerField(default=1, verbose_name=_("antal talade gånger"))  # Is set to 0 when speaking
    has_spoken = models.BooleanField(default=False, verbose_name=_("har talat?"))

    objects = SpeakerListManager()

    def __str__(self):
        return str(self.event) + " | " + str(self.user)
