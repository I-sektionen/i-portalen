from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime
from tags.models import Tag
from .managers import ArticleManager
from utils.validators import less_than_160_characters_validator
from utils.time import now_plus_one_month


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

    author = models.CharField(max_length=255,
                              verbose_name='skribent',
                              help_text="Skribent av texten")

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='användare',
                             help_text="Användaren som skrivit texten")
    tags = models.ManyToManyField(Tag, verbose_name='tag', blank=True)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    replacing = models.ForeignKey('self', null=True, blank=True, default=None)
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

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artiklar"
        permissions = (('can_approve_article', 'Can approve article'),)