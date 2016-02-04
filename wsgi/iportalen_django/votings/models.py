from django.db import models
from django.utils.translation import ugettext_lazy as _


class QuestionGroup(models.Model):
    pass

class Question(models.Model):
    name = models.CharField(verbose_name=_('namn'), max_length=255)
    body = models.TextField(
        verbose_name=_("Utförligare information"),
        help_text=_("Utförligare information som ."))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("fråga")
        verbose_name_plural = _("frågor")

class Answers(models.Model):
    pass
