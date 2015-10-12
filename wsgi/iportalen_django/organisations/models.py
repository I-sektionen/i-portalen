from django.conf import settings
from django.db import models
from django.utils.http import urlquote
from django.contrib.auth.models import Group
from tags.models import Tag
from utils.validators import slash_validator


# Create your models here.
class Organisation(models.Model):
    NOT_IN_MENU = "N"
    SEKTIONEN = "S"
    FORENINGAR = "F"
    UTSKOTT = "U"
    ORGANISATION_TYPE_CHOICES = (
        (NOT_IN_MENU, "Inte i menyn"),
        (SEKTIONEN, "Sektionen"),
        (FORENINGAR, "Föreningar"),
        (UTSKOTT, "Utskott"),
    )
    IMAGE_HEIGHT = 320
    IMAGE_WIDTH = 480


    name = models.CharField(verbose_name='Namn',
                            help_text="Namn för organisationen",
                            max_length=255,
                            unique=True,
                            null=False,
                            validators=[slash_validator])
    description = models.TextField(verbose_name='Beskrivning',
                                   help_text="Beskrivning av organisationen",
                                   null=True,
                                   blank=True)
    contact_info = models.TextField(verbose_name='Kontaktinformation',
                                    help_text="Kontaktinformation för organisationen",
                                    null=True,
                                    blank=True)
    image = models.FileField(verbose_name='Bild',
                             help_text="Bild för organisationen",
                             upload_to="organisations",
                             null=True,
                             blank=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name='Ledare',
                               help_text="Ledare för organisationen",
                               null=True,
                               blank=True,
                               related_name="leader")
    organisation_type = models.CharField(verbose_name='Meny',
                                         help_text="Under vilken menyrubrik ska organisationen ligga, "
                                                   "(Gäller inte om en föräldrar organisation är vald)",
                                         max_length=1,
                                         choices=ORGANISATION_TYPE_CHOICES,
                                         default=NOT_IN_MENU)
    parent_organisation = models.ForeignKey('self',
                                            verbose_name='Föräldrar organisation',
                                            help_text="Organisation under vilken denna organisation ligger",
                                            null=True,
                                            blank=True,
                                            related_name="parent")
    group = models.ForeignKey(Group,
                              verbose_name='Grupp',
                              help_text="Grupp knuten till organisationen",
                              null=True,
                              blank=True,
                              related_name="group")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/organisations/{:}/".format(urlquote(self.name))