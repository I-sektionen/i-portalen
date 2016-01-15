from django.contrib.sites.models import Site
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from utils.validators import less_than_160_characters_validator
from organisations.models import Organisation
from tags.models import Tag
from .exceptions import CouldNotRegisterException
from .managers import SpeakerListManager


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
    headline = models.CharField(
        verbose_name='arrangemangets namn',
        help_text="Ge ditt evenemang en titel, till exempel 'Excelutbildning med Knowit'",
        max_length=255)
    lead = models.TextField(
        verbose_name='kort beskrivning',
        help_text="Ge en kort beskrivning av ditt event. Max 160 tecken. Tex. 'Få cellsynt kompetens med Knowit!'",
        validators=[less_than_160_characters_validator])
    body = models.TextField(
        verbose_name='beskrivning',
        help_text="Beskrivning av eventet")
    location = models.CharField(
        max_length=30,
        verbose_name="plats",
        help_text="Plats för eventet tex. C1 eller Märkesbacken")

    start = models.DateTimeField(
        verbose_name='starttid',
        help_text="När startar arrangemanget?")  # When the event starts.
    end = models.DateTimeField(
        verbose_name='sluttid',
        help_text="När slutar arrangemanget?")  # When the event ends.

    enable_registration = models.BooleanField(
        verbose_name='användare kan anmäla sig')
    registration_limit = models.PositiveIntegerField(
        verbose_name='antal platser', help_text="Hur många kan anmäla sig?", blank=True, null=True)

    extra_deadline = models.DateTimeField(
        verbose_name='extra anmälningsstopp',
        help_text="Exempelvis: Datum att anmäla sig innan för att få mat. Kan lämnas tomt.",
        blank=True,
        null=True)
    extra_deadline_text = models.CharField(
        max_length=255,
        verbose_name="beskrivning till det extra anmälningsstoppet",
        help_text="Ex. få mat, garanteras fika osv. Lämna tomt om extra anmälningsstopp ej angivits.",
        blank=True,
        null=True)
    # Dagar innan start för avanmälan. Räknas bakåt från 'start'
    deregister_delta = models.PositiveIntegerField(
        verbose_name='Sista dag för använmälan',
        default=1,
        help_text="Sista dag för avanmälan i antal dagar innan eventet")

    visible_from = models.DateTimeField(
        verbose_name="Datum för publicering")

    #  Access rights
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='användare', null=True,
        on_delete=models.SET_NULL)  # User with admin rights/creator.
    # The group which has admin rights. If left blank is it only the user who can admin.
    tags = models.ManyToManyField(
        Tag, verbose_name='tag', blank=True,
        help_text="Håll ner Ctrl för att markera flera.")

    status = models.CharField(
        max_length=1, choices=STATUSES, default=DRAFT, blank=False, null=False)
    rejection_message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    replacing = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    organisations = models.ManyToManyField(
        Organisation,
        blank=True,
        default=None,
        verbose_name='arrangör',
        help_text="Organisation(er) som arrangerar evenemanget. Medlemmar i dessa kan senare ändra eventet. Håll ner Ctrl för att markera flera.")
    sponsored = models.BooleanField(verbose_name='sponsrat', default=False, help_text="Kryssa i om innehållet är sponsrat")
    ###########################################################################
    # Meta data for model
    ###########################################################################
    class Meta:
        verbose_name = "Arrangemang"
        verbose_name_plural = "Arrangemang"
        permissions = (('can_approve_event', 'Can approve event'),)

    ###########################################################################
    # Overridden and standard functions
    ###########################################################################

    def save(self, *args, **kwargs):
        """Override save to set created and modifed date before saving."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        """Return string representation of object"""
        return self.headline

    def get_absolute_url(self):
        """Get url of object"""
        return "/event/%i/" % self.id

    ###########################################################################
    # Properties reachable in template
    ###########################################################################

    def _type(self):
        """Return model name"""
        return "event"

    type = property(_type)

    @property
    def preregistrations(self):
        """Returns list of preregistered users."""
        query = EntryAsPreRegistered.objects.filter(event=self)
        user_list = []
        for el in query:
            user_list.append(el.user)
        return user_list

    @property
    def reserves(self):
        """Returns list of reserve users."""
        q = EntryAsReserve.objects.filter(event=self)
        user_list = []
        for el in q:
            user_list.append(el.user)
        return user_list

    @property
    def participants(self):
        """Returns list of participating users."""
        q = EntryAsParticipant.objects.filter(event=self)
        user_list = []
        for el in q:
            user_list.append(el.user)
        return user_list

    @property
    def number_of_preregistrations(self):
        """Returns number of preregistered users."""
        return EntryAsPreRegistered.objects.filter(event=self).count()

    @property
    def number_of_reserves(self):
        """Returns number of reserve users."""
        return EntryAsReserve.objects.filter(event=self).count()

    @property
    def number_of_checked_in_participants(self):
        """Returns number of participating users."""
        return EntryAsParticipant.objects.filter(event=self).count()

    @property
    def no_show(self):
        preregistered = EntryAsPreRegistered.objects.filter(event=self)
        participants = EntryAsParticipant.objects.filter(event=self)
        preregistered_list=[]
        participant_list=[]
        for p in preregistered:
            preregistered_list.append(p.user)
        for p in participants:
            participant_list.append(p.user)
        no_show = set(preregistered_list).difference(set(participant_list))
        return no_show

    # Is the event full?
    @property
    def full(self):
        """Check if the event full"""
        return self.number_of_preregistrations >= self.registration_limit

    @property
    def entry_deadline(self):
        """Returns the register deadline"""
        return self.start - timezone.timedelta(days=self.deregister_delta)

    @property
    def can_deregister(self):
        """Check if register deadline have passed"""
        return self.start - timezone.timedelta(days=self.deregister_delta) > timezone.now()

    ###########################################################################
    # Member function
    ###########################################################################

    def reserves_object(self):
        return EntryAsReserve.objects.filter(event=self)

    def register_user(self, user):
        """This method determines if a specific user can register to an event."""
        # possible to register?
        if not self.enable_registration:
            raise CouldNotRegisterException(event=self, reason="registering är avstängd")

        # Already registered?
        try:
            EntryAsPreRegistered.objects.get(event=self, user=user)
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
            entry = EntryAsReserve.objects.get(user=user, event=self)
            entry.delete()
        except ObjectDoesNotExist:
            pass

    @transaction.atomic
    def deregister_user(self, user):
        # Deregistration time has passed.
        if not self.can_deregister:
            return CouldNotRegisterException(event=self, reason="avanmälningstiden har passerats")
        found = False
        try:
            entry = EntryAsPreRegistered.objects.get(event=self, user=user)
            entry.delete()
            reserves = EntryAsReserve.objects.filter(event=self).order_by("timestamp")
            if reserves.exists():
                user = reserves[0]
                self.register_user(reserves[0].user)
                subject = "Du har blivit uppflyttad från reservlistan!"
                body = "".join(["<p>Grattis!</p>",
                                "<p>Du har blivit uppflyttad från reservlistan och är nu anmäld till {event}.</p>",
                                "<p>Vill du inte ha din plats kan du avanmäla dig på länken ",
                                "<a href='{site}{link}'>{site}{link}</a></p>"]
                               ).format(event=self.headline,
                                        site=Site.objects.get_current().domain,
                                        link=self.get_absolute_url())
                send_mail(subject, "", settings.EMAIL_HOST_USER, [user.user.email, ], fail_silently=False, html_message=body)
                user.delete()
            found = True
        except ObjectDoesNotExist:
            pass
        if not found:
            try:
                entry = EntryAsReserve.objects.get(event=self, user=user)
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

    def reserve(self, user):
        if user in self.reserves:
            return True
        return False

    def reserve_nr(self, user):
        return self.reserves_object().get(userREJE=user).position()

    def check_in(self, user):
        if user in self.participants:
            raise CouldNotRegisterException(event=self, reason="Du är redan anmäld som deltagare")
        participant = EntryAsParticipant(user=user, event=self)
        participant.save()
        participant.add_speech_nr()

    def can_administer(self, user):
        if not user.is_authenticated():
            return False
        event_orgs = self.organisations.all()
        user_orgs = user.get_organisations()
        intersection = set(event_orgs).intersection(user_orgs)
        # Like a venn diagram where the intersections is the organisations that both the user and the event have.
        if intersection:
            return True
        if self.user == user:
            return True
        if user.has_perm("events.can_approve_event"):
            return True
        return False

    def get_new_status(self, draft):
        try:
            s_db = Event.objects.get(pk=self.pk)
            if s_db.status == Event.DRAFT:
                if draft:
                    return {"new": False, "status": Event.DRAFT}
                else:
                    return {"new": False, "status": Event.BEING_REVIEWED}
            elif s_db.status == Event.BEING_REVIEWED:
                if draft:
                    return {"new": False, "status": Event.DRAFT}
                else:
                    return {"new": False, "status": Event.BEING_REVIEWED}
            elif s_db.status == Event.APPROVED:
                if draft:
                    return {"new": True, "status": Event.DRAFT}
                else:
                    return {"new": True, "status": Event.BEING_REVIEWED}
            elif s_db.status == Event.REJECTED:
                if draft:
                    return {"new": False, "status": Event.DRAFT}
                else:
                    return {"new": False, "status": Event.BEING_REVIEWED}
        except:
            if draft:
                return {"new": False, "status": Event.DRAFT}
            else:
                return {"new": False, "status": Event.BEING_REVIEWED}

    # Rejects an event from being published, attaches message if present.
    def reject(self, user, msg=None):
        if not user.has_perm('events.can_approve_event'):
            return False
        if self.status == Event.BEING_REVIEWED:
            if msg:
                send_mail(
                    "Ditt event har blivit avslaget.",
                    "",
                    settings.EMAIL_HOST_USER,
                    [self.user.email, ],
                    fail_silently=False,
                    html_message="<p>Ditt event {head} har blivit avslaget med motiveringen:</p><p>{msg}</p>".format(
                        head=self.headline, msg=msg))
            self.rejection_message = msg
            self.status = Event.REJECTED
            self.save()
            return True
        return False

    # Approves the event.
    @transaction.atomic
    def approve(self, user):
        if self.status == Event.BEING_REVIEWED and user.has_perm('events.can_approve_event'):
            self.status = Event.APPROVED
            self.save()
            if self.replacing:

                exclude = ["event",
                           "entryasreserve",
                           "entryaspreregistered",
                           "entryasparticipant",
                           "speakerlist",
                           "id",
                           "created",
                           "modified",
                           "replacing"]
                multi = ["tags", "organisations"]
                for field in self.replacing._meta.get_fields():
                    if field.name not in exclude:
                        if field.name not in multi:
                            setattr(self.replacing, field.name, getattr(self, field.name))
                        else:
                            getattr(self.replacing, field.name).clear()
                            setattr(self.replacing, field.name, getattr(self, field.name).all())
                self.delete()
                self.replacing.save()
            return True
        return False

    # Add speaker
    # remove speaker
    # Move up speaker
    # Move down
    # Clear list
    # Get all

    def get_user_from_speech_nr(self, speech_nr):
        return self.entryasparticipant_set.get(speech_nr=speech_nr)

    def get_speech_num_from_user(self, user):
        return self.entryasparticipant_set.get(user=user).speech_nr

    def add_speaker_to_queue(self, speech_nr):
        u = self.get_user_from_speech_nr(speech_nr=speech_nr).user
        first_object = not SpeakerList.objects.filter(event=self).exists()
        if not first_object:
            last = SpeakerList.objects.get(event=self, next_speaker=None)
            s = SpeakerList.objects.create(user=u, event=self)
            s.first = False
            last.next_speaker = s
            last.save()
        else:
            s = SpeakerList.objects.create(user=u, event=self)
            s.first = True
        s.save()
        return True

    def clear_speaker_queue(self):
        q = SpeakerList.objects.filter(event=self)
        for element in q:
            element.delete()

    def remove_first_speaker_from_queue(self):
        sp = SpeakerList.objects.get_first(event=self)
        if sp.next_speaker is not None:
            sp.next_speaker.first = True
            sp.next_speaker.save()
        sp.delete()

    def remove_speaker_from_queue(self, speech_nr):
        u = self.get_user_from_speech_nr(speech_nr=speech_nr).user
        to_remove = SpeakerList.objects.filter(event=self, user=u)
        for ele in to_remove:
            self._remove_speaker_from_queue(ele)

    def _remove_speaker_from_queue(self, to_remove):
        before = None
        after = None
        try:
            before = SpeakerList.objects.get(next_speaker=to_remove)
        except ObjectDoesNotExist:
            pass
        try:
            after = to_remove.next_speaker
        except ObjectDoesNotExist:
            pass
        if (before is None) and (after is not None):
            # First element of several
            after.first = True
            after.save()
        elif (before is not None) and (after is not None):
            # Middle element
            before.next_speaker = after
            before.save()
        # Case: Single element, last element.
        to_remove.delete()

    def get_speaker_queue(self):
        try:
            first = SpeakerList.objects.get(event=self, first=True)
        except ObjectDoesNotExist:
            return []

        result = [{'first_name': first.user.first_name,
                   'last_name': first.user.last_name}]
        next_speaker = first.next_speaker
        while next_speaker is not None:
            result.append({'first_name': next_speaker.user.first_name,
                           'last_name': next_speaker.user.last_name})
            next_speaker = next_speaker.next_speaker
        return result


######################################################################
#  Entry models are used for the logic behind users standing in line  #
######################################################################

# Used to track the order of reserves for an event.
class EntryAsReserve(models.Model):
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def position(self):
        entries = EntryAsReserve.objects.filter(event=self.event).order_by("timestamp")

        for pos, entry in enumerate(entries):
            if entries[pos].user == self.user:
                return pos + 1
        return None

    class Meta:
        verbose_name = "Reserv"
        verbose_name_plural = "Reserver"

    def __str__(self):
        return str(self.user) + " reserv på " + str(self.event)


# Used to track the pre-registered users for an event.
class EntryAsPreRegistered(models.Model):
    event = models.ForeignKey(Event, verbose_name='arrangemang', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare', null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    no_show = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Anmälning"
        verbose_name_plural = "Anmälningar"

    def __str__(self):
        return str(self.user) + " anmäld på: " + str(self.event)


# Used to track the people check in on an event. (Actually participating)
class EntryAsParticipant(models.Model):
    event = models.ForeignKey(Event, verbose_name="arrangemang", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare', null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    speech_nr = models.PositiveIntegerField(verbose_name="talar nummer", null=True, blank=True)

    class Meta:
        verbose_name = "Deltagare"
        verbose_name_plural = "Deltagare"

    def __str__(self):
        return str(self.event) + " | " + str(self.user)

    def add_speech_nr(self):
        try:
            self.speech_nr = EntryAsParticipant.objects.filter(event_id=self.event_id).order_by('-speech_nr')[
                                 0].speech_nr + 1
        except:
            self.speech_nr = 1
        self.save()


class SpeakerList(models.Model):
    event = models.ForeignKey(Event, verbose_name="arrangemang", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare', null=True, on_delete=models.SET_NULL)
    first = models.NullBooleanField(default=None)
    next_speaker = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_NULL)

    objects = SpeakerListManager()

    def move_up(self):
        if self.first:
            return
        # Find event above and switch order
        above = SpeakerList.objects.get(next_speaker=self)
        above.next_speaker = self.next_speaker
        self.next_speaker = above
        if above.first:
            self.first = True
            above.first = False
        self.save()
        above.save()

    def move_down(self):
        if self.next_speaker is None:
            return
        below = self.next_speaker
        if self.first:
            if below is None:
                return
            self.next_speaker = below.next_speaker
            below.next_speaker = self
            below.first = True
        else:
            above = SpeakerList.object.get(next_speaker=self)
            above.next_speaker = below
            self.next_speaker = below.next_speaker
            below.next_speaker = self
            above.save()
        self.save()
        below.save()

    def __str__(self):
        return str(self.event) + " | " + str(self.user)
