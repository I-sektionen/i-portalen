from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from tags.models import Tag
from .exceptions import CouldNotRegisterException
# A user can register and deregister
# The admin can:
# - Change properties of an event
# - Check-in users
# - See all participants during the event (if check-in is used)
# - See all pre-registrations
# - See all reserves.


class Event(models.Model):
# Event model which holds basic data about an event.
    headline = models.CharField(verbose_name='rubrik', max_length=255)
    lead = models.TextField(verbose_name='ingress', )
    body = models.TextField(verbose_name='brödtext', )

    visible_from = models.DateTimeField()
    visible_to = models.DateTimeField()
    approved = models.BooleanField(verbose_name='godkänd', default=False )

    # access  # TODO: access restrictions

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')  # User with admin rights/creator.
    # The group which has admin rights. If left blank is it only the user who can admin.
    admin_group = models.ForeignKey(Group, blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='tag', blank=True)

    location = models.CharField(max_length=30)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    start = models.DateTimeField(verbose_name='start')  # When the event starts.
    end = models.DateTimeField(verbose_name='slut')  # When the event ends.
    published_from = models.DateTimeField(verbose_name='anmälningsstart', null=True, blank=True)  # When event is published

    enable_registration = models.BooleanField(verbose_name='kan anmäla sig')
    # "start - deregister_delta" gives last dergistration date+time, defaults to one day.
    deregister_delta = models.DurationField(verbose_name='anmälningsslut', default=timezone.timedelta(days=1))
    registration_limit = models.IntegerField(verbose_name='max antal anmälningar', blank=True, null=True)

    @property
    def preregistrations(self):
        q = EntryAsPreRegistered.objects.filter(event__exact=self)
        return q

    @property
    def reserves(self):
        q = EntryAsReserve.objects.filter(event__exact=self)
        return q

    @property
    def participants(self):
        q = EntryAsParticipant.objects.filter(event__exact=self)
        return q

    @property
    def number_of_preregistrations(self):
        return EntryAsPreRegistered.objects.filter(event__exact=self).count()

    @property
    def number_of_reserves(self):
        return EntryAsReserve.objects.filter(event__exact=self).count()

    @property
    def number_of_checked_in_participants(self):
        return EntryAsParticipant.objects.filter(event__exact=self).count()

    #  This method determines if a specific user can register to an event.
    def register_user(self, user):

        # possible to register?
        if not self.enable_registration:
            raise CouldNotRegisterException(event=self, reason="registering är avstängd")

        # To many participants?
        if self.number_of_preregistrations >= self.registration_limit:
            raise CouldNotRegisterException(event=self, reason="maxantalet deltagare är uppnått")

        # Has the start date passed?
        if self.start < timezone.now():
            raise CouldNotRegisterException(event=self, reason="starttiden har passerats")

        EntryAsPreRegistered(user=user, event=self).save()

    def deregister_user(self, user):
        # Deregistration time has passed.
        if self.start-self.deregister_delta < timezone.now():
            return CouldNotRegisterException(event=self, reason="avanmälningstiden har passerats")
        found = False
        try:
            entry = EntryAsPreRegistered.objects.get(event__exact=self, user__exact=user)
            entry.delete()
            found = True
        except ObjectDoesNotExist:
            pass
        if not found:
            try:
                entry = EntryAsReserve.objects.get(event__exact=self, user__exact=user)
                entry.delete()
                found = True
            except ObjectDoesNotExist:
                pass
        return found

    def can_administer(self, user):
        if user != self.user:
            if self.admin_group is None:
                return False
            elif self.admin_group not in user.groups:  # I LOVE PYTHON <3
                return False
        return True

    class Meta:
        verbose_name = "Arrangemang"
        verbose_name_plural = "Arrangemang"
        permissions = (('can_approve_article', 'Can approve article'),)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline


######################################################################
#  Entry models are used for the logic behind users standing in line  #
######################################################################

# Used to track the order of reserves for an event.
class EntryAsReserve(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reserv"
        verbose_name_plural = "Reserver"

    def __str__(self):
        return str(self.user) + " reserv på " + str(self.event)


# Used to track the pre-registered users for an event.
class EntryAsPreRegistered(models.Model):
    event = models.ForeignKey(Event, verbose_name='arrangemang')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')
    timestamp = models.DateTimeField(auto_now_add=True)
    no_show = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Anmälning"
        verbose_name_plural = "Anmälningar"

    def __str__(self):
        return str(self.user) + " anmäld på: " + str(self.event)


# Used to track the people check in on an event. (Actually participating)
class EntryAsParticipant(models.Model):
    event = models.ForeignKey(Event, verbose_name="arrangemang")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Deltagare"
        verbose_name_plural = "Deltagare"

    def __str__(self):
        return str(self.event) + " | " + str(self.user)