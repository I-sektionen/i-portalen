from django.db import models
from articles.models import Tag, Article
from iportalen import settings


class Event(Article):
    start = models.DateTimeField(verbose_name='start')
    end = models.DateTimeField(verbose_name='slut')
    enable_registration = models.BooleanField(verbose_name='kan anmäla sig')
    registration_limit = models.IntegerField(verbose_name='max antal anmälningar')

    class Meta:
        verbose_name = "Arrangemang"
        verbose_name_plural = "Arrangemanger"


class EntryDeadline(models.Model):
    description_sv = models.TextField(verbose_name='beskrivning')
    entry_from = models.DateTimeField(verbose_name='anmälningsstart')
    entry_to = models.DateTimeField(verbose_name='anmälningsslut')
    event = models.ForeignKey(Event, verbose_name='arrangemang')
    enable_unregistration = models.BooleanField(verbose_name='kan avanmäla sig')

    class Meta:
        verbose_name = "Anmälningsperiod"
        verbose_name_plural = "Anmälningsperioder"


class Entry(models.Model):
    event = models.ForeignKey(Event, verbose_name='arrangemang')
    deadline = models.ForeignKey(EntryDeadline, verbose_name='anmälningsperiod')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')
    registered_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Anmälning"
        verbose_name_plural = "Anmälningar"
