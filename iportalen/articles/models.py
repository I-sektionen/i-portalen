from django.db import models
import datetime
from django.contrib.auth.models import User
from iportalen import settings

class Tag(models.Model):
    name_sv = models.CharField(verbose_name='namn', max_length=255)

    def __str__(self):
        return self.name_sv

    class Meta:
        verbose_name = "tagg"
        verbose_name_plural = "taggar"


class Article(models.Model):
    headline = models.CharField(verbose_name='rubrik', max_length=255)
    lead = models.TextField(verbose_name='ingress', )
    body = models.TextField(verbose_name='brödtext', )

    visible_from = models.DateTimeField()
    visible_to = models.DateTimeField()
    approved = models.BooleanField(verbose_name='godkänd', )
    # access  # TODO: access restrictions

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')
    tags = models.ManyToManyField(Tag, verbose_name='tag')

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artiklar"