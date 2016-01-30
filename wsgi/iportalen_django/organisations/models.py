from django.core.urlresolvers import reverse
from django.db import models
from django.utils.http import urlquote
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from utils.validators import slash_validator


# Create your models here.
class Organisation(models.Model):
    NOT_IN_MENU = "N"
    SEKTIONEN = "S"
    FORENINGAR = "F"
    ORGANISATION_TYPE_CHOICES = (
        (NOT_IN_MENU, _("Inte i menyn")),
        (SEKTIONEN, _("Sektionen")),
        (FORENINGAR, _("Föreningar")),
    )

    name = models.CharField(verbose_name=_("Namn"),
                            help_text=_("Namn för organisationen"),
                            max_length=255,
                            unique=True,
                            null=False,
                            validators=[slash_validator])
    description = models.TextField(verbose_name=_("Beskrivning"),
                                   help_text=_("Beskrivning av organisationen"),
                                   null=True,
                                   blank=True)
    contact_info = models.TextField(verbose_name=_("Kontaktinfo"),
                                    help_text=_("Kontaktinformation för organisationen"),
                                    null=True,
                                    blank=True)
    image = models.FileField(verbose_name=_("Bild"),
                             help_text=_("Bild för organisationen"),
                             upload_to="organisations",
                             null=True,
                             blank=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_("Ledare"),
                               help_text=_("Ledare för organisationen"),
                               null=True,
                               blank=True,
                               related_name="leader",
                               on_delete=models.SET_NULL)
    organisation_type = models.CharField(verbose_name=_("Meny"),
                                         help_text=_("Under vilken menyrubrik ska organisationen ligga, "
                                                   "(Välj samma som hos föräldrar organisationen om en sådan är vald)"),
                                         max_length=1,
                                         null=True,
                                         blank=False,
                                         choices=ORGANISATION_TYPE_CHOICES,
                                         default=NOT_IN_MENU)
    parent_organisation = models.ForeignKey('self',
                                            verbose_name=_("Föräldrar organisation"),
                                            help_text=_("Organisation under vilken denna organisation ligger"),
                                            null=True,
                                            blank=True,
                                            related_name="parent",
                                            on_delete=models.SET_NULL)
    group = models.ForeignKey(Group,
                              verbose_name=_("Grupp"),
                              help_text=_("Grupp knuten till organisationen"),
                              null=True,
                              blank=True,
                              related_name="group",
                              on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("organisation")
        verbose_name_plural = _("organisationer")

    def __str__(self):
        return self.name

    def get_absolute_url(self):

        return reverse('organisations:organisation', kwargs={'organisation_name': urlquote(self.name)})

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
                            verbose_name=_("Posten medlemmen har i organisationen"))

    email = models.EmailField(verbose_name=_("Emailadress"),
                              help_text=_("Email som är specifik för posten."),
                              blank=True,
                              null=True)

    org = models.ForeignKey(Organisation,
                            null=False,
                            blank=False,
                            verbose_name=_("Medlemmens organisation"),
                            )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=False,
                             blank=False,
                             verbose_name=_("Användare"))

    class Meta:
        verbose_name = _("Organisations post")
        verbose_name_plural = _("Organisations poster")

    def __str__(self):
        return self.post + " (i " + str(self.org) + ")"
