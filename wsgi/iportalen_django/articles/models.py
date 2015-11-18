from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime
import os
from tags.models import Tag
from .managers import ArticleManager
from utils.validators import less_than_160_characters_validator
from utils.time import now_plus_one_month
from organisations.models import Organisation


class Article(models.Model):
    headline = models.CharField(verbose_name='rubrik',
                                max_length=255,
                                help_text="Rubriken till artikeln")
    lead = models.TextField(verbose_name='ingress',
                            help_text="Ingressen är den text som syns i nyhetsflödet. Max 160 tecken.",
                            validators=[less_than_160_characters_validator])
    body = models.TextField(verbose_name='brödtext',
                            help_text="Brödtext syns när en artikel visas enskilt.")

    visible_from = models.DateTimeField(verbose_name='publicering',
                                        help_text="Publiceringsdatum",
                                        default=datetime.datetime.now)
    visible_to = models.DateTimeField(verbose_name='avpublicering',
                                      help_text="Avpubliceringsdatum",
                                      default=now_plus_one_month)
    draft = models.BooleanField(verbose_name='utkast', default=False,
                                help_text="Sparar utan att publicera")
    approved = models.BooleanField(verbose_name='godkänd', default=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='användare',
                             help_text="Användaren som skrivit texten",
                             null=True,
                             on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, verbose_name='tag', help_text="Använd Ctrl- alt. Cmd-knapp för att markera flera taggar.", blank=True)

    attachment = models.FileField(verbose_name='Bifogad fil',
                             help_text="Bifogad fil för artikel",
                             upload_to="article_attachments",
                             null=True,
                             blank=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    replacing = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    organisations = models.ManyToManyField(Organisation,
                                           blank=False,
                                           verbose_name='organisationer',
                                           help_text="Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln.")
    objects = ArticleManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return "/articles/%i/" % self.id

    def filename(self):
        return os.path.basename(self.attachment.name)


    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artiklar"
        permissions = (('can_approve_article', 'Can approve article'),)

    def has_permission_to_change(self, user):
        a_org = self.organisations.all()
        user_orgs = user.get_organisations()
        intersection = set(a_org).intersection(user_orgs)
        has_perm_to_edit = False
        if intersection:
            has_perm_to_edit = True
        if self.user == user:  # Add "and not a_org" if you want to only be able to change as user if no organisation is choosen.
            has_perm_to_edit = True
        if user.has_perm("articles.can_approve_article"):
            has_perm_to_edit = True
        return has_perm_to_edit

