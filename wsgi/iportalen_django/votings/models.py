from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from events.models import Event
from iportalen import settings
from utils import time
from .exceptions import CouldNotVoteException


class QuestionGroup(models.Model):
    EVENT = 'e'
    ALL = 'a'
    STATUSES = (
        (EVENT, _("Incheckade deltagare på ett event kan rösta.")),
        (ALL, _("Alla medlemmar kan rösta")),
    )

    question_status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=EVENT,
        blank=False,
        null=False)
    event = models.ForeignKey(Event, verbose_name=_('event'), blank=True, null=True)
    visible_from = models.DateTimeField(
        verbose_name=_("publicering"),
        help_text=_("Publiceringsdatum"),
        default=time.now)
    visible_to = models.DateTimeField(
        verbose_name=_("avpublicering"),
        help_text=_("Avpubliceringsdatum"),
        default=time.now_plus_one_month)

    def __str__(self):
        return "id: {pk}".format(pk=self.pk)

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('votings:question group', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("frågegrupp")
        verbose_name_plural = _("frågegrupper")


class Question(models.Model):
    OPEN = 'o'
    CLOSED = 'c'
    STATUSES = (
        (OPEN, _("Öppen")),
        (CLOSED, _("Stängd")),
    )
    PUBLIC_DETAILED = 'd'
    PUBLIC_LIMITED = 'l'
    PRIVATE = 'p'
    RESULT = (
        (PUBLIC_DETAILED, _("Publik tillgång till detaljerad information om röstingen.")),
        (PUBLIC_LIMITED, _("Publik tillgång till begränsad information om röstningen.")),
        (PRIVATE, _("Privat åtkomst enbart för administratörer")),
    )
    question_group = models.ForeignKey(QuestionGroup, verbose_name=_('frågegrupp'),)
    name = models.CharField(verbose_name=_('namn'), max_length=255)
    body = models.TextField(verbose_name=_("utförlig information"), help_text=_("Utförligare information till frågan."))
    result = models.CharField(
        max_length=1,
        choices=RESULT,
        default=PRIVATE,
        blank=False,
        null=False)
    question_status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=CLOSED,
        blank=False,
        null=False)
    nr_of_picks = models.IntegerField(verbose_name=_("Antal val en användare kan kryssa i på frågan."), default=1)
    anonymous = models.BooleanField(verbose_name=_('namn'), default=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("användare"),
        help_text=_("Användaren som ändrat på frågan."),
        null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('votings:question', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("fråga")
        verbose_name_plural = _("frågor")


class Options(models.Model):
    name = models.CharField(verbose_name=_("alternativ"), max_length=255)
    question = models.ForeignKey(Question, verbose_name=_("fråga"))

    def __str__(self):
        return "{question}, {name}".format(name=self.name, question=self.question.name)

    class Meta:
        verbose_name = _("alternativ")
        verbose_name_plural = _("alternativen")


class Votes(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("fråga"))
    option = models.ForeignKey(Options, verbose_name=_("alternativ"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("användare"), null=True, blank=True)

    class Meta:
        verbose_name = _("röst")
        verbose_name_plural = _("röster")

    def save(self, *args, **kwargs):
        if not self.question.hasvoted_set.filter(user=self.user).exists():
            if self.question.anonymous and self.user:
                self.user = None
            super(Votes, self).save(*args, **kwargs)
        else:
            raise CouldNotVoteException(reason=ugettext("User has already voted."))


class HasVoted(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("fråga"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("användare"))

    class Meta:
        verbose_name = _("deltagare i omröstningen")
        verbose_name_plural = _("deltagarna i omröstningen")
