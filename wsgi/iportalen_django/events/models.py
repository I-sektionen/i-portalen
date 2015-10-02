from django.db import models
from django.conf import settings
from django.utils import timezone


from tags.models import Tag
from .exceptions import CouldNotRegisterException


class Event(models.Model):
    headline = models.CharField(verbose_name='rubrik', max_length=255)
    lead = models.TextField(verbose_name='ingress', )
    body = models.TextField(verbose_name='brödtext', )

    visible_from = models.DateTimeField()
    visible_to = models.DateTimeField()
    approved = models.BooleanField(verbose_name='godkänd', default=False )

    # access  # TODO: access restrictions

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')
    tags = models.ManyToManyField(Tag, verbose_name='tag', blank=True)

    location = models.CharField(max_length=30)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    start = models.DateTimeField(verbose_name='start')
    end = models.DateTimeField(verbose_name='slut')

    enable_registration = models.BooleanField(verbose_name='kan anmäla sig')
    registration_limit = models.IntegerField(verbose_name='max antal anmälningar', blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="participates_on",
                                          verbose_name="deltagare",
                                          blank=True)

    # This method determines if a specific user can register to an event.
    def register_user(self, user):

        # possible to register?
        if not self.enable_registration:
            raise CouldNotRegisterException(event=self, reason="registering är avstängd")

        # To many participants?
        if self.participants.count() >= self.registration_limit:
            raise CouldNotRegisterException(event=self, reason="maxantalet deltagare är uppnått")

        # Has the start date passed?
        if self.start < timezone.now():
            raise CouldNotRegisterException(event=self, reason="starttiden har passerats")

        self.participants.add(user)



    class Meta:
        verbose_name = "Arrangemang"
        verbose_name_plural = "Arrangemanger"
        permissions = (('can_approve_article', 'Can approve article'),)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline


class EntryDeadline(models.Model):
    description = models.TextField(verbose_name='beskrivning')
    entry_from = models.DateTimeField(verbose_name='anmälningsstart')
    entry_to = models.DateTimeField(verbose_name='anmälningsslut')
    event = models.ForeignKey(Event, verbose_name='arrangemang')
    enable_unregistration = models.BooleanField(verbose_name='kan avanmäla sig')

    class Meta:
        verbose_name = "Anmälningsperiod"
        verbose_name_plural = "Anmälningsperioder"

    def __str__(self):
        return str(self.event) + " | " + self.description


class Entry(models.Model):
    event = models.ForeignKey(Event, verbose_name='arrangemang')
    deadline = models.ForeignKey(EntryDeadline, verbose_name='anmälningsperiod')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')
    registered_time = models.DateTimeField(auto_now_add=True)
    no_show = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Anmälning"
        verbose_name_plural = "Anmälningar"

    def __str__(self):
        return str(self.event) + " | " + str(self.user)