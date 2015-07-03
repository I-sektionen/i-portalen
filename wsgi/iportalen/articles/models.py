from django.db import models
from django.utils import timezone
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(verbose_name='namn', max_length=255)

    def __str__(self):
        return "<a href='" + self.get_absolute_url() + "/'>" + self.name + "</a>"

    def get_absolute_url(self):
        return "/tag/%i/" % self.id

    class Meta:
        verbose_name = "tagg"
        verbose_name_plural = "taggar"


class Article(models.Model):
    headline = models.CharField(verbose_name='rubrik', max_length=255)
    lead = models.TextField(verbose_name='ingress', )
    body = models.TextField(verbose_name='brödtext', )

    visible_from = models.DateTimeField()
    visible_to = models.DateTimeField()
    approved = models.BooleanField(verbose_name='godkänd', default=False )

    # access  # TODO: access restrictions

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='användare')
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

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artiklar"
        permissions = (('can_approve_article', 'Can approve article'),)