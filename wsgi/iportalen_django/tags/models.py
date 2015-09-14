from django.db import models
from django.contrib.auth.models import Group


class Tag(models.Model):
    name = models.CharField(verbose_name='namn', max_length=255, unique=True)
    group = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/articles/tag/%s/" % self.name

    class Meta:
        verbose_name = "tagg"
        verbose_name_plural = "taggar"
