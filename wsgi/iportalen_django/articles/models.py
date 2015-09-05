from django.db import models
from django.utils import timezone
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(verbose_name='namn', max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/articles/tag/%s/" % self.name

    class Meta:
        verbose_name = "tagg"
        verbose_name_plural = "taggar"


class Article(models.Model):
    headline = models.CharField(verbose_name='rubrik',
                                max_length=255,
                                help_text="Rubriken till Artikeln")
    lead = models.TextField(verbose_name='ingress',
                            help_text="Ingress som syns utan att klicka på artikeln.")
    body = models.TextField(verbose_name='brödtext',
                            help_text="Brödtext som syns efter att ha klickat på läs mer.")

    visible_from = models.DateTimeField(verbose_name='publicering',
                                        help_text="Datum för publicering")
    visible_to = models.DateTimeField(verbose_name='avpublicering',
                                      help_text="Datum för avpublicering.")
    draft = models.BooleanField(verbose_name='utkast', default=False,
                                help_text="Utkast kommer inte att publiceras")
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