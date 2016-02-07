from django.db import models
from utils.validators import slash_validator
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    name = models.CharField(verbose_name=_('namn'), max_length=255, unique=True, validators=[slash_validator])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("tagg")
        verbose_name_plural = _("taggar")
