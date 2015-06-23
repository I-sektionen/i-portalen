from django.db import models
import datetime
from django.contrib.auth.models import User
from iportalen import settings

class Tag(models.Model):
    name_sv = models.CharField(verbose_name='namn', max_length=255)
    name_en = models.CharField(verbose_name='name', max_length=255)

    def __str__(self):
        return self.name_sv

    class Meta:
        verbose_name = "tagg"
        verbose_name_plural = "taggar"


class Article(models.Model):
    headline_sv = models.CharField(verbose_name='rubrik', max_length=255)
    lead_sv = models.TextField(verbose_name='ingress', )
    body_sv = models.TextField(verbose_name='brödtext', )

    headline_en = models.CharField(verbose_name='headline', max_length=255)
    lead_en = models.TextField(verbose_name='lead')
    body_en = models.TextField(verbose_name='body')

    visible_from = models.DateTimeField(verbose_name='publicera från', default=datetime.datetime.now())
    visible_to = models.DateTimeField(verbose_name='publicera till', default=datetime.datetime.now().year+1)
    approved = models.BooleanField(verbose_name='godkänd', )
    # access  # TODO: access restrictions

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')
    tags = models.ManyToManyField(Tag, verbose_name='tag')

    created = models.DateTimeField(verbose_name='skapad', editable=False)
    updated = models.DateTimeField(verbose_name='uppdaterad', editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline_sv


    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artiklar"