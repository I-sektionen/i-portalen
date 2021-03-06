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
from tags.models import Tag
from .managers import AlumniManager
from organisations.models import Organisation


class Alumni_Article(models.Model):

    ARTIKEL = 'a'
    ARRANGEMANG = 'e'

    TYPES = (
        (ARTIKEL, _('Artikel')),
        (ARRANGEMANG, _('Event'))
    )

    headline = models.CharField(
        verbose_name=_("rubrik"),
        max_length=255,
        help_text=_("Rubriken till artikeln"))
    lead = models.TextField(
        verbose_name=_("ingress"),
        help_text=_("Ingressen är den text som syns i nyhetsflödet. Max 160 tecken."),
        validators=[less_than_160_characters_validator])
    body = models.TextField(
        verbose_name=_("brödtext"),
        help_text=_("Brödtext syns när en artikel visas enskilt."))
    visible_from = models.DateTimeField(
        verbose_name=_("publicering"),
        help_text=_("Publiceringsdatum"),
        default=time.now)
    visible_to = models.DateTimeField(
        verbose_name=_("avpublicering"),
        help_text=_("Avpubliceringsdatum"),
        default=time.now_plus_one_month)
    rejection_message = models.TextField(blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("användare"),
        help_text=_("Användaren som skrivit texten"),
        null=True,
        on_delete=models.SET_NULL)
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("tag"),
        blank=True,
        help_text=_("Håll ner Ctrl för att markera flera."))

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    replacing = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL)

    kind = models.CharField(
        max_length=1,
        choices=TYPES,
        default=ARTIKEL,
        verbose_name=_("Typ"),
        help_text=_("Välj om du vill skapa en artikel eller ett event."))
    organisations = models.ManyToManyField(
        Organisation,
        blank=True,
        verbose_name=_("organisationer"),
        help_text=_("Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln."
                   " Håll ner Ctrl för att markera flera."))

    objects = AlumniManager()  # Manager

    ###########################################################################
    # Meta data for model
    ###########################################################################
    class Meta:
        verbose_name = _("Artikel/Event")
        verbose_name_plural = _("Artiklar/Event")
        permissions = (('can_approve_article', 'Can approve article'),)

    ###########################################################################
    # Overridden and standard functions
    ###########################################################################

    def save(self, *args, **kwargs):
        """Override save to set created and modifed date before saving."""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Alumni_Article, self).save(*args, **kwargs)

    def __str__(self):
        """Return string representation of object"""
        return self.headline

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('alumni_portal:alumni_article', kwargs={'pk': self.pk})

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
        if (self.visible_to) > timezone.now():
            return True
        return False
    ###########################################################################
    # Member function
    ###########################################################################

    def filename(self):
        return os.path.basename(self.attachment.name)

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


class Magazine(models.Model):

    title = models.CharField(
        verbose_name=_("titel"),
        max_length=255,
        help_text=_("Titel på tidningen")
    )

    url = models.URLField(
        verbose_name=_("URL"),
        help_text=_("URL till tidningen")
    )

    thumbnail = models.TextField(
        verbose_name=_("thumbnail"),
        help_text=_("thumbnail som ska visas"),
        default=_("https://www.rosegoldstudio.com/wp-content/plugins/penci-portfolio//images/no-thumbnail.jpg")
    )

    date = models.DateField(
        verbose_name=_("utgivningsdatum"),
        help_text=_("utgivningsdatum för tidningen")
    )

    class Meta:
        verbose_name = _("Tidning")
        verbose_name_plural = _("Tidningar")

    def __str__(self):
        """Return string representation of object"""
        return self.title