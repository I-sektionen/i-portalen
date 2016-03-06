import os
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from utils.validators import less_than_160_characters_validator
from organisations.models import Organisation
from tags.models import Tag
from .exceptions import CouldNotRegisterException
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.files.base import ContentFile
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from PIL import Image
import io
from tags.models import Tag
from organisations.models import Organisation
from .managers import EventManager, EntryAsPreRegisteredManager
from datetime import timedelta


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
    CANCEL = 'c'
    BEING_CANCELD = 'e'
    STATUSES = (
        (DRAFT, _("utkast")),
        (BEING_REVIEWED, _("väntar på godkännande")),
        (REJECTED, _("Avslaget")),
        (APPROVED, _("Godkänt")),
        (CANCEL, _("Inställt")),
        (BEING_CANCELD, _("väntar på att bli inställd"))
    )


    #  Description:
    headline = models.CharField(
        verbose_name=_("arrangemangets namn"),
        help_text=_("Ge ditt evenemang en titel, till exempel 'Excelutbildning med Knowit'"),
        max_length=255)
    lead = models.TextField(
        verbose_name=_("kort beskrivning"),
        help_text=_("Ge en kort beskrivning av ditt event. Max 160 tecken. Tex. 'Få cellsynt kompetens med Knowit!'"),
        validators=[less_than_160_characters_validator])
    body = models.TextField(
        verbose_name=_("beskrivning"),
        help_text=_("Beskrivning av eventet"))
    location = models.CharField(
        max_length=30,
        verbose_name=_("plats"),
        help_text=_("Plats för eventet tex. C1 eller Märkesbacken"))

    start = models.DateTimeField(
        verbose_name=_("starttid"),
        help_text=_("När startar arrangemanget?"))  # When the event starts.
    end = models.DateTimeField(
        verbose_name=_("sluttid"),
        help_text=_("När slutar arrangemanget?"))  # When the event ends.

    enable_registration = models.BooleanField(
        verbose_name=_("användare kan anmäla sig"))
    registration_limit = models.PositiveIntegerField(
        verbose_name=_("antal platser"), help_text=_("Hur många kan anmäla sig?"), blank=True, null=True)

    extra_deadline = models.DateTimeField(
        verbose_name=_("extra anmälningsstopp"),
        help_text=_("Exempelvis: Datum att anmäla sig innan för att få mat. Kan lämnas tomt."),
        blank=True,
        null=True)
    extra_deadline_text = models.CharField(
        max_length=255,
        verbose_name=_("beskrivning till det extra anmälningsstoppet"),
        help_text=_("Ex. få mat, garanteras fika osv. Lämna tomt om extra anmälningsstopp ej angivits."),
        blank=True,
        null=True)
    # Dagar innan start för avanmälan. Räknas bakåt från 'start'
    deregister_delta = models.PositiveIntegerField(
        verbose_name=_("Sista dag för anmälan/avanmälan"),
        default=1,
        help_text=_("Sista dag för anmälan/avanmälan i antal dagar innan eventet"))

    visible_from = models.DateTimeField(
        verbose_name=_("Datum för publicering"))

    #  Access rights
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("användare"), null=True,
        on_delete=models.SET_NULL)  # User with admin rights/creator.
    # The group which has admin rights. If left blank is it only the user who can admin.
    tags = models.ManyToManyField(
        Tag, verbose_name=_("tag"), blank=True,
        help_text=_("Håll ner Ctrl för att markera flera."))

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
        verbose_name=_("arrangör"),
        help_text=_("Organisation(er) som arrangerar evenemanget. "
                    "Medlemmar i dessa kan senare ändra eventet. Håll ner Ctrl för att markera flera."))
    sponsored = models.BooleanField(
        verbose_name=_("sponsrat"), default=False, help_text=_("Kryssa i om innehållet är sponsrat"))

    finished = models.BooleanField(verbose_name='Avsluta event', default=False, help_text="Kryssa i om eventet ska avslutas")

    objects = EventManager()

    ###########################################################################
    # Meta data for model
    ###########################################################################

    class Meta:
        verbose_name = _("Arrangemang")
        verbose_name_plural = _("Arrangemang")
        permissions = (('can_approve_event', 'Can approve event'), ('can_view_no_shows', 'Can view no shows'), ('can_remove_no_shows', 'Can remove no shows'))

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
        return reverse('events:event', kwargs={'pk': self.pk})

    ###########################################################################
    # Properties reachable in template
    ###########################################################################

    def _type(self):
        """Return model name"""
        return "event"

    type = property(_type)

    @property
    def filename(self):
        return os.path.basename(self.attachment.name)

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
        preregistered_list = []
        participant_list = []
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

    @property
    def show_event_before_experation(self):
        """Returns the end date + three dates to hinder people from accesing the event through URL, unless admin"""
        if (self.end + timedelta(days=3)) > timezone.now():
            return True
        return False

    ###########################################################################
    # Member function
    ###########################################################################

    def reserves_object(self):
        return EntryAsReserve.objects.filter(event=self)

    def register_user(self, user):
        """This method determines if a specific user can register to an event."""
        # possible to register?
        if not self.enable_registration:
            raise CouldNotRegisterException(event=self, reason=ugettext("registering är avstängd"))

        # Already registered?
        try:
            EntryAsPreRegistered.objects.get(event=self, user=user)
            raise CouldNotRegisterException(event=self, reason=ugettext("du är redan registrerad"))
        except ObjectDoesNotExist:
            pass

        # To many participants?
        if self.number_of_preregistrations >= self.registration_limit:
            raise CouldNotRegisterException(event=self, reason=ugettext("maxantalet deltagare är uppnått"))

        # Has the start date passed?
        if self.start < timezone.now():
            raise CouldNotRegisterException(event=self, reason=ugettext("starttiden har passerats"))

        # Has the register date passed?
        if not self.can_deregister:
            raise CouldNotRegisterException(event=self, reason="anmälningstiden har passerats")
        # Is the user banned from event registration?
        if len(EntryAsPreRegistered.objects.get_noshow(user=user)) >= 3:
            raise CouldNotRegisterException(event=self, reason="du har missat 3 event")

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
            return CouldNotRegisterException(event=self, reason=ugettext("avanmälningstiden har passerats"))
        found = False
        try:
            entry = EntryAsPreRegistered.objects.get(event=self, user=user)
            entry.delete()
            reserves = EntryAsReserve.objects.filter(event=self).order_by("timestamp")
            if reserves.exists():
                user = reserves[0]
                self.register_user(reserves[0].user)
                subject = ugettext("Du har blivit uppflyttad från reservlistan!")
                body = "".join(["<p>",
                                ugettext("Grattis!"),
                                "</p><p>",
                                ugettext("Du har blivit uppflyttad från reservlistan och är nu anmäld till"),
                                " {event}.</p><p>",
                                ugettext("Vill du inte ha din plats kan du avanmäla dig på länken"),
                                " <a href='{site}{link}'>{site}{link}</a></p>"]
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
            raise CouldNotRegisterException(event=self, reason=ugettext("du är redan registrerad som reserv"))

        if user in self.participants:
            raise CouldNotRegisterException(event=self, reason=ugettext("du är anmäld som deltagare"))

        # Is the user banned from event registration?
        if len(EntryAsPreRegistered.objects.get_noshow(user=user)) >= 3:
            raise CouldNotRegisterException(event=self, reason="du har missat 3 event")

        # Register as reserve
        entry = EntryAsReserve(event=self, user=user)
        entry.save()
        return entry

    def registered(self, user):
        if (user in self.preregistrations) or (user in self.reserves):
            return True
        return False

    def is_checked_in(self, user):
        if user in self.participants:
            return True
        return False

    def reserve(self, user):
        if user in self.reserves:
            return True
        return False

    def reserve_nr(self, user):
        return self.reserves_object().get(userREJE=user).position()

    @transaction.atomic
    def check_in(self, user):
        if user in self.participants:
            raise CouldNotRegisterException(event=self, reason=ugettext("Du är redan anmäld som deltagare"))
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

    def get_new_status(self, draft):  # TODO: Reduce complexity
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
                    ugettext("Ditt event har blivit avslaget."),
                    "",
                    settings.EMAIL_HOST_USER,
                    [self.user.email, ],
                    fail_silently=False,
                    html_message="".join(["<p>",
                                          ugettext("Ditt event"),
                                          " {head} ",
                                          ugettext("har blivit avslaget med motiveringen:"),
                                          "</p><p>{msg}</p>"]).format(
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
                           "replacing",
                           "imageattachment",
                           "otherattachment",
                           "questiongroup"]
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


###########################################################################
# Attachment Models
###########################################################################


def _image_file_path(instance, filename):
    """Returns the subfolder in which to upload images for event. This results in media/event/img/<filename>"""
    return os.path.join(
        'event', str(instance.event.pk), 'images', filename
    )


THUMB_SIZE = (129, 129)  # Size of saved thumbnails.


class ImageAttachment(models.Model):
    """Used to handle image attachments to be shown in the event"""
    img = models.ImageField(
        upload_to=_image_file_path,
        null=False,
        blank=False,
        verbose_name='eventlbild'
    )
    thumbnail = models.ImageField(
        upload_to=_image_file_path,
        null=True,
        blank=True,
        verbose_name='förhandsvisning'
    )
    caption = models.CharField(max_length=100)
    event = models.ForeignKey(Event,
                              null=False,
                              blank=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='användare',
        help_text="Uppladdat av.",
        null=True,
        on_delete=models.SET_NULL,
        related_name='event_image_uploader')

    def _set_thumbnail(self):
        path = self.img.path
        try:
            image = Image.open(path)
        except IOError:
            print("Could not open!")
            raise
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        thumb_name_path, thumb_extension = os.path.splitext(self.img.name)
        thumb_extension = thumb_extension.lower()
        a, thumb_name = os.path.split(thumb_name_path)
        thumb_file_name = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            print('Wrong file extension!')
            return False    # Unrecognized file type

        temp_thumb = io.BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.thumbnail.save(thumb_file_name, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        return True

    def save(self, *args, **kwargs):
        super(ImageAttachment, self).save(*args, **kwargs)
        self._set_thumbnail()
        super(ImageAttachment, self).save(*args, **kwargs)
        # It first saves the model to set and save the main img.
        # Then it generates the thumbnail _without_ saving. The instance holds the thumbnail.
        # Then it it saves again. So the new field is saved also.
        # This is because it seems the model must be saved once in order to open the img and generate the thumbnail.
        #
        #  There is probably a much nicer way to do this. (This is replicated in articles)

    def __str__(self):
        return os.path.basename(self.img.name) + " (Event: " + str(self.article.pk) + ")"


# Clean up when model is removed
@receiver(pre_delete, sender=ImageAttachment)
def other_attachment_delete(sender, instance, **kwargs):
    instance.img.delete(False)  # False avoids saving the model.
    instance.thumb.delete(False)


def _file_path(instance, filename):
    return os.path.join(
        'event', str(instance.event.pk), 'attachments', filename
    )


class OtherAttachment(models.Model):
    """"Regular attachments such as pdf:s and it's like."""

    file = models.FileField(
        upload_to=_file_path,
        null=False,
        blank=False,
        verbose_name='eventlbilaga',
    )
    display_name = models.CharField(max_length=160, null=False, blank=False)
    file_name = models.CharField(max_length=300, null=False, blank=True)
    event = models.ForeignKey(Event, null=False, blank=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='användare',
        help_text="Uppladdat av.",
        null=True,
        on_delete=models.SET_NULL,
        related_name='event_attachment_uploader')

    def save(self, *args, **kwargs):
        self.file_name = os.path.basename(self.file.name)
        super(OtherAttachment, self).save(*args, **kwargs)

    def __str__(self):
        return self.display_name + " (" + self.file_name + ")" + "för event: " + str(self.article)


#  This receiver part here makes sure to remove files if the model instance is deleted.
@receiver(pre_delete, sender=OtherAttachment)
def other_attachment_delete(sender, instance, **kwargs):
    instance.file.delete(False)  # False avoids saving the model.


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
        verbose_name = _("Reserv")
        verbose_name_plural = _("Reserver")

    def __str__(self):
        return str(self.user) + ugettext(" reserv på ") + str(self.event)


# Used to track the pre-registered users for an event.
class EntryAsPreRegistered(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("arrangemang"), null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("användare"), null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    no_show = models.BooleanField(default=False)

    objects = EntryAsPreRegisteredManager()

    class Meta:
        verbose_name = _("Anmälning")
        verbose_name_plural = _("Anmälningar")

    def __str__(self):
        return str(self.user) + ugettext(" anmäld på: ") + str(self.event)


# Used to track the people check in on an event. (Actually participating)
class EntryAsParticipant(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("arrangemang"), null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("användare"), null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    speech_nr = models.PositiveIntegerField(verbose_name=_("talar nummer"), null=True, blank=True)

    class Meta:
        verbose_name = _("Deltagare")
        verbose_name_plural = _("Deltagare")

    def __str__(self):
        return str(self.event) + " | " + str(self.user)

    def add_speech_nr(self):
        try:
            self.speech_nr = EntryAsParticipant.objects.filter(event_id=self.event_id).order_by('-speech_nr')[
                                 0].speech_nr + 1
        except:
            self.speech_nr = 1
        self.save()


