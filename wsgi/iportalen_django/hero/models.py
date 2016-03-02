import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from iportalen import settings
from utils import time


def _file_path(instance, filename):
    return os.path.join(
        'hero', filename
    )


class Hero(models.Model):

    file = models.FileField(
        upload_to=_file_path,
        null=False,
        blank=False,
        verbose_name='Hero',
    )
    file_name = models.CharField(max_length=300, null=False, blank=True)
    visible_from = models.DateTimeField(
        verbose_name=_("publicering"),
        help_text=_("Publiceringsdatum"),
        default=time.now)

    modified = models.DateTimeField(editable=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='användare',
        help_text="Uppladdat av.",
        null=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Hero")
        verbose_name_plural = _("Herosarna")  # Det ska stavas så! :P
        ordering = ['modified']

    def save(self, *args, **kwargs):
        self.file_name = os.path.basename(self.file.name)
        self.modified = timezone.now()
        super(Hero, self).save(*args, **kwargs)

    def __str__(self):
        return self.file_name


#  This receiver part here makes sure to remove files if the model instance is deleted.
@receiver(pre_delete, sender=Hero)
def other_attachment_delete(sender, instance, **kwargs):
    instance.file.delete(False)  # False avoids saving the model.
