# Add article and event class from
# from wsgi.iportalen_django.articles.models import Article
# and same but event or create new slim classes?
from django.db import models, transaction
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
import os
from django.utils.translation import ugettext_lazy as _
from utils.validators import less_than_160_characters_validator
from utils import time
from .managers import ThesisManager
from organisations.models import Organisation


class Thesis_Article(models.Model):

    company = models.CharField(
        verbose_name=_("företagsnamn"),
        max_length=255,
        help_text=_("Annonseringsföretagets namn"))
    headline = models.CharField(
        verbose_name=_("rubrik"),
        max_length=255,
        help_text=_("Rubriken till annonsen"))
    lead = models.TextField(
        verbose_name=_("ingress"),
        help_text=_("Ingressen är den text som syns i nyhetsflödet. Max 160 tecken."),
        validators=[less_than_160_characters_validator])
    body = models.TextField(
        verbose_name=_("brödtext"),
        help_text=_("Brödtext syns när annonsen visas enskilt."))
    location = models.CharField(
        verbose_name=_("ort"),
        max_length=64,
        help_text=_("Ort"))
    payed = models.BooleanField(
        verbose_name=_("betalt"),
        default=False,
        help_text=_("Kryssa i om exjobbet är betalt"))
    visible_from = models.DateTimeField(
        verbose_name=_("publicering"),
        help_text=_("Publiceringsdatum"),
        default=time.now)
    visible_to = models.DateTimeField(
        verbose_name=_("avpublicering"),
        help_text=_("Avpubliceringsdatum"),
        default=time.now_plus_one_month)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("användare"),
        help_text=_("Användaren som skrivit texten"),
        null=True,
        on_delete=models.SET_NULL)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    organisations = models.ManyToManyField(
        Organisation,
        blank=True,
        verbose_name=_("organisationer"),
        help_text=_("Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln."
                    " Håll ner Ctrl för att markera flera."))

    objects = ThesisManager()  # Manager

    ###########################################################################
    # Meta data for model
    ###########################################################################
    class Meta:
        verbose_name = _("Annons")
        verbose_name_plural = _("Annonser")
        permissions = (('can_approve_thesis_article', 'Can approve thesis articles'),)

    ###########################################################################
    # Overridden and standard functions
    ###########################################################################

    def save(self, *args, **kwargs):
        """Override save to set created and modifed date before saving."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Thesis_Article, self).save(*args, **kwargs)

    def __str__(self):
        """Return string representation of object"""
        return self.headline

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('thesis_portal:thesis_article', kwargs={'pk': self.pk})

    ###########################################################################
    # Properties reachable in template
    ###########################################################################

    def _type(self):
        """Return model name"""
        return "article"

    type = property(_type)

    @property
    def show_article_before_experation(self):
        """Returns the end date to hinder people from accesing the article through URL, unless admin"""
        if self.visible_to > timezone.now():
            return True
        return False
    ###########################################################################
    # Member function
    ###########################################################################

    def can_administer(self, user):
        if not user.is_authenticated():
            return False
        article_orgs = self.organisations.all()
        user_orgs = user.get_organisations()
        intersection = set(article_orgs).intersection(user_orgs)
        # Like a venn diagram where the intersections is the organisations that both the user and the event have.
        if intersection:
            return True
        if self.user == user:
            return True
        if user.has_perm("articles.can_approve_article"):
            return True
        return False
