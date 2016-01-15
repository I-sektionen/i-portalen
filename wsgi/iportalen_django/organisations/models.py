from django.conf import settings
from django.db import models
from django.utils.http import urlquote
from django.contrib.auth.models import Group
from django.conf import settings
from utils.validators import slash_validator


# Create your models here.
class Organisation(models.Model):
    NOT_IN_MENU = "N"
    SEKTIONEN = "S"
    FORENINGAR = "F"
    ORGANISATION_TYPE_CHOICES = (
        (NOT_IN_MENU, "Inte i menyn"),
        (SEKTIONEN, "Sektionen"),
        (FORENINGAR, "Föreningar"),
    )

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
    contact_info = models.TextField(verbose_name='Kontaktinfo',
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
                               related_name="leader",
                               on_delete=models.SET_NULL)
    organisation_type = models.CharField(verbose_name='Meny',
                                         help_text="Under vilken menyrubrik ska organisationen ligga, "
                                                   "(Välj samma som hos föräldrar organisationen om en sådan är vald)",
                                         max_length=1,
                                         null=True,
                                         blank=False,
                                         choices=ORGANISATION_TYPE_CHOICES,
                                         default=NOT_IN_MENU)
    parent_organisation = models.ForeignKey('self',
                                            verbose_name='Föräldrar organisation',
                                            help_text="Organisation under vilken denna organisation ligger",
                                            null=True,
                                            blank=True,
                                            related_name="parent",
                                            on_delete=models.SET_NULL)
    group = models.ForeignKey(Group,
                              verbose_name='Grupp',
                              help_text="Grupp knuten till organisationen",
                              null=True,
                              blank=True,
                              related_name="group",
                              on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "organisation"
        verbose_name_plural = "organisationer"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/organisations/{:}/".format(urlquote(self.name))

    def can_edit(self, user):
        if user == self.leader:
            return True
        elif user.has_perm("organisations.change_organisation"):
            return True
        return False

    def user_in_organisation(self, user):
        try:
            self.organisationpost_set.get(user=user)
            return True
        except:
            return False


class OrganisationPost(models.Model):
    post = models.CharField(max_length=40,
                            blank=True,
                            null=True,
                            verbose_name="Posten medlemmen har i organisationen")

    email = models.EmailField(verbose_name="Emailadress",
                              help_text="Email som är specifik för posten.",
                              blank=True,
                              null=True)

    org = models.ForeignKey(Organisation,
                            null=False,
                            blank=False,
                            verbose_name="Medlemmens organisation",
                            )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=False,
                             blank=False,
                             verbose_name="Användare")

    class Meta:
        verbose_name = "Organisations post"
        verbose_name_plural = "Organisations poster"

    def __str__(self):
        return self.post + " (i " + str(self.org) + ")"
