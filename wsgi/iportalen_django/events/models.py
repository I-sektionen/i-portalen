from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from utils.validators import less_than_160_characters_validator
from organisations.models import Organisation

from tags.models import Tag
from .exceptions import CouldNotRegisterException
# A user can register and deregister
# The admin can:
# - Change properties of an event
# - Check-in users
# - See all participants during the event (if check-in is used)
# - See all pre-registrations
# - See all reserves.


# Event model which holds basic data about an event.
class Event(models.Model):
    # Internal:
    DRAFT = 'd'
    BEING_REVIEWED = 'b'
    REJECTED = 'r'
    APPROVED = 'a'
    STATUSES = (
        (DRAFT, 'utkast'),
        (BEING_REVIEWED, 'väntar på godkännande'),
        (REJECTED, 'Avslaget'),
        (APPROVED, 'Godkännt')
    )

    #  Description:
    headline = models.CharField(verbose_name='arrangemangets namn',help_text="Ge ditt evenemang en titel, till exempel 'Excelutbildning med Knowit'", max_length=255)
    lead = models.TextField(verbose_name='kort beskrivning', help_text="Ge en kort beskrivning av ditt event. Max 160 tecken. Tex. 'Få cellsynt kompetens med Knowit!'", validators=[less_than_160_characters_validator])
    body = models.TextField(verbose_name='beskrivning', help_text="Beskrivning av eventet")
    location = models.CharField(max_length=30, verbose_name="plats", help_text="Plats för eventet tex. C1 eller Märkesbacken")

    start = models.DateTimeField(verbose_name='starttid', help_text="När startar arrangemanget?")  # When the event starts.
    end = models.DateTimeField(verbose_name='sluttid', help_text="När slutar arrangemanget?")  # When the event ends.

    enable_registration = models.BooleanField(verbose_name='användare kan anmäla sig')
    registration_limit = models.PositiveIntegerField(verbose_name='antal platser', help_text="Hur många kan anmäla sig?" ,blank=True, null=True)

    # Dagar innan start för avanmälan. Räknas bakåt från 'start'
    deregister_delta = models.PositiveIntegerField(verbose_name='Sista dag för använmälan',
                                                   default=1,
                                                   help_text="Sista dag för avanmälan i antal dagar innan eventet")

    visible_from = models.DateTimeField(verbose_name="Datum för publicering")

    #  Access rights
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')  # User with admin rights/creator.
    # The group which has admin rights. If left blank is it only the user who can admin.
    admin_group = models.ForeignKey(Group, blank=True, null=True,
                                    verbose_name="grupp som kan administrera eventet.",
                                    help_text="Utöver den användare som nu skapar eventet.")
    tags = models.ManyToManyField(Tag, verbose_name='tag', blank=True)

    status = models.CharField(max_length=1, choices=STATUSES, default=DRAFT, blank=False, null=False)
    rejection_message = models.TextField(blank=True, null=True)
    #approved = models.BooleanField(verbose_name='godkänd', default=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    organisations = models.ManyToManyField(Organisation,
                                           blank=True,
                                           default=None,
                                           verbose_name='organisationer',
                                           help_text="Organisation/organisationer som artikeln hör till" )
    @property
    def preregistrations(self):
        query = EntryAsPreRegistered.objects.filter(event__exact=self)
        list = []
        for el in query:
            list.append(el.user)
        return list

    @property
    def reserves(self):
        q = EntryAsReserve.objects.filter(event__exact=self)
        list = []
        for el in q:
            list.append(el.user)
        return list

    def reserves_object(self):
        return EntryAsReserve.objects.filter(event__exact=self)


    @property
    def participants(self):
        q = EntryAsParticipant.objects.filter(event__exact=self)
        list = []
        for el in q:
            list.append(el.user)
        return list

    @property
    def number_of_preregistrations(self):
        return EntryAsPreRegistered.objects.filter(event__exact=self).count()

    @property
    def number_of_reserves(self):
        return EntryAsReserve.objects.filter(event__exact=self).count()

    @property
    def number_of_checked_in_participants(self):
        return EntryAsParticipant.objects.filter(event__exact=self).count()

    # Is the event full?
    @property
    def full(self):
        return self.number_of_preregistrations >= self.registration_limit

    #  This method determines if a specific user can register to an event.
    def register_user(self, user):

        # possible to register?
        if not self.enable_registration:
            raise CouldNotRegisterException(event=self, reason="registering är avstängd")

        # Already registered?
        try:
            EntryAsPreRegistered.objects.get(event__exact=self, user__exact=user)
            raise CouldNotRegisterException(event=self, reason="du är redan registrerad")
        except ObjectDoesNotExist:
            pass

        # To many participants?
        if self.number_of_preregistrations >= self.registration_limit:
            raise CouldNotRegisterException(event=self, reason="maxantalet deltagare är uppnått")

        # Has the start date passed?
        if self.start < timezone.now():
            raise CouldNotRegisterException(event=self, reason="starttiden har passerats")

        EntryAsPreRegistered(user=user, event=self).save()
        try:
            entry = EntryAsReserve.objects.get(user__exact=user, event__exact=self)
            entry.delete()
        except ObjectDoesNotExist:
            pass

    @property
    def can_deregister(self):
        return self.start-timezone.timedelta(days=self.deregister_delta) > timezone.now()

    def deregister_user(self, user):
        # Deregistration time has passed.
        if not self.can_deregister:
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

    def register_reserve(self, user):
        # Check for weirdness:
        if user in self.reserves:
            raise CouldNotRegisterException(event=self, reason="du är redan registrerad som reserv")

        if user in self.participants:
            raise CouldNotRegisterException(event=self, reason="du är anmäld som deltagare")

        # Register as reserve
        entry = EntryAsReserve(event=self, user=user)
        entry.save()
        return entry

    def registered(self, user):
        if (user in self.preregistrations) or (user in self.reserves):
            return True
        return False

    def check_in(self, user):
        if user in self.participants:
            raise CouldNotRegisterException(event=self, reason="Du är redan anmäld som deltagare")
        EntryAsParticipant(user=user, event=self).save()

    def can_administer(self, user):
        if not user.is_authenticated():
            return False
        if user != self.user:
            try:
                if user.groups is None:
                    return False
                if self.admin_group is None:
                    return False
                elif self.admin_group not in user.groups:  # I LOVE PYTHON <3
                    return False
            except:
                return False
        return True

    #  This method changes the event status to approval mode.
    def send_to_approval(self, user):
        if user != self.user:
            return False
        if self.status == Event.DRAFT or self.status == Event.REJECTED:
            self.status = Event.BEING_REVIEWED
            self.save()
            return True
        else:
            return False

    # Rejects an event from being published, attaches message if present.
    def reject(self, user, msg=None):
        if not user.has_perm('events.can_approve_event'):
            return False
        if self.status == Event.BEING_REVIEWED:
            self.rejection_message = msg
            self.status = Event.REJECTED
            self.save()
            return True
        return False

    # Approves the event.
    def approve(self, user):
        if self.status == Event.BEING_REVIEWED and user.has_perm('events.can_approve_event'):
            self.status = Event.APPROVED
            self.save()
            return True
        return False

    class Meta:
        verbose_name = "Arrangemang"
        verbose_name_plural = "Arrangemang"
        permissions = (('can_approve_event', 'Can approve event'),)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return "/event/%i/" % self.id


######################################################################
#  Entry models are used for the logic behind users standing in line  #
######################################################################

# Used to track the order of reserves for an event.
class EntryAsReserve(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def position(self):
        entries = EntryAsReserve.objects.filter(event__exact=self.event).order_by("timestamp")

        for pos, entry in enumerate(entries):
            if entries[pos] == entry:
                return pos+1
        return None

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
