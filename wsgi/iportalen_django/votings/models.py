from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _, ugettext
from events.models import Event
from iportalen import settings
from organisations.models import Organisation
from utils import time
from .exceptions import CouldNotVoteException
from .managers import QuestionGroupManager, QuestionManager


class QuestionGroup(models.Model):
    EVENT = 'e'
    ALL = 'a'
    STATUSES = (
        (EVENT, _("Incheckade deltagare på ett event kan rösta.")),
        (ALL, _("Alla medlemmar kan rösta")),
    )
    name = models.CharField(verbose_name=_('namn'), max_length=255, blank=True, null=True)
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
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("skapare"), null=True, blank=False)
    organisations = models.ManyToManyField(
        Organisation,
        blank=True,
        default=None,
        verbose_name=_("administrerar"),
        help_text=_("Organisation(er) som administrerar frågeguppen, Håll ner Ctrl för att markera flera."))
    objects = QuestionGroupManager()

    def __str__(self):
        if self.question_status == self.EVENT:
            return self.event.headline
        elif self.name:
            return self.name
        else:
            return "Question group: {pk}".format(pk=self.pk)

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('votings:question group', kwargs={'qg_pk': self.pk})

    class Meta:
        verbose_name = _("frågegrupp")
        verbose_name_plural = _("frågegrupper")

    def can_administer(self, user):
        if not user.is_authenticated():
            return False
        qg_orgs = self.organisations.all()
        user_orgs = user.get_organisations()
        intersection = set(qg_orgs).intersection(user_orgs)
        # Like a venn diagram where the intersections is the organisations that both the user and the event have.
        if intersection:
            return True
        if self.creator == user:
            return True
        return False


class Question(models.Model):
    DRAFT = 'd'
    OPEN = 'o'
    CLOSED = 'c'
    STATUSES = (
        (DRAFT, _("Utkast")),
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
    BEFORE = 'b'
    AFTER = 'a'
    ON_CLOSE = 'c'
    PUBLISH_RESULT_OPTIONS = (
        (BEFORE, _("Gör resultaten synliga innan man röstat.")),
        (AFTER, _("Gör resultaten synliga efter att man röstat.")),
        (ON_CLOSE, _("Gör resultaten synliga när röstningen stängt.")),
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
    publish_results = models.CharField(
        max_length=1,
        choices=PUBLISH_RESULT_OPTIONS,
        default=ON_CLOSE,
        blank=False,
        null=False)
    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=DRAFT,
        blank=False,
        null=False)
    nr_of_picks = models.IntegerField(verbose_name=_("Antal val en användare kan kryssa i på frågan."), default=1)
    anonymous = models.BooleanField(verbose_name=_('anonym'), default=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("användare"),
        help_text=_("Användaren som ändrat på frågan."),
        null=True,
        on_delete=models.SET_NULL)

    objects = QuestionManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('votings:question', kwargs={'qg_pk': self.question_group_id, 'q_pk': self.pk})

    def get_absolute_result_url(self):
        """Get url of object"""
        return reverse('votings:result', kwargs={'qg_pk': self.question_group_id, 'q_pk': self.pk})

    class Meta:
        verbose_name = _("fråga")
        verbose_name_plural = _("frågor")

    def voters(self):
        if self.question_group.question_status == QuestionGroup.EVENT:
            return self.question_group.event.entryasparticipant_set.values_list('user')
        elif self.question_group.question_status == QuestionGroup.ALL:
            return settings.AUTH_USER_MODEL.objects.all()

    def is_voter(self, user):
        return self.voters().filter(user=user).exists()

    def has_voted(self, user):
        return self.hasvoted_set.filter(user=user).exists()

    def can_vote(self, user):
        return self.is_voter(user) and not self.has_voted(user) and self.status == self.OPEN

    def show_result(self, user):
        if self.result == self.PUBLIC_DETAILED or self.result == self.PUBLIC_LIMITED:
            if self.publish_results == self.ON_CLOSE:
                if self.status == self.CLOSED:
                    return True
                else:
                    return False
            elif self.publish_results == self.BEFORE:
                return True
            elif self.publish_results == self.AFTER:
                if self.has_voted(user):
                    return True
                else:
                    return False
        else:
            return False


    @transaction.atomic
    def vote(self, user, options):
        if not self.is_voter(user):
            raise CouldNotVoteException(reason=_("Du kan inte rösta i den här frågan."))
        if self.has_voted(user):
            raise CouldNotVoteException(reason=_("Du har redan röstat i den här frågan."))
        if self.status != self.OPEN:
            raise CouldNotVoteException(reason=_("Frågan är inte längre öppen för omröstning."))
        if len(options) > self.nr_of_picks:
            raise CouldNotVoteException(reason=_("Du har valt för många alternativ."))
        for option in options:
            Vote.objects.create(question=self, option_id=option, user=user)
        HasVoted.objects.create(question=self, user=user)


class Option(models.Model):
    name = models.CharField(verbose_name=_("alternativ"), max_length=255)
    question = models.ForeignKey(Question, verbose_name=_("fråga"))

    def __str__(self):
        return "{question}, {name}".format(name=self.name, question=self.question.name)

    class Meta:
        verbose_name = _("alternativ")
        verbose_name_plural = _("alternativen")


class Vote(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("fråga"))
    option = models.ForeignKey(Option, verbose_name=_("alternativ"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("användare"), null=True, blank=True)

    class Meta:
        verbose_name = _("röst")
        verbose_name_plural = _("röster")

    def save(self, *args, **kwargs):
        if self.question.anonymous and self.user:
            self.user = None
        super(Vote, self).save(*args, **kwargs)


class HasVoted(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("fråga"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("användare"))

    class Meta:
        verbose_name = _("deltagare i omröstningen")
        verbose_name_plural = _("deltagarna i omröstningen")
