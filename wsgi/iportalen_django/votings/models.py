from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import Count
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
    SUPER_PRIVATE = 's'
    RESULT = (
        (PUBLIC_DETAILED, _("Publik tillgång till detaljerad information om röstingen.")),
        (PUBLIC_LIMITED, _("Publik tillgång till begränsad information om röstningen.")),
        (PRIVATE, _("Privat åtkomst enbart för administratörer")),
        (SUPER_PRIVATE, _("Privat åtkomst enbart för personer listade i \"Användare som kan se resultatet\"")),
    )
    BEFORE = 'b'
    AFTER = 'a'
    ON_CLOSE = 'c'
    PUBLISH_RESULT_OPTIONS = (
        (BEFORE, _("Gör resultaten synliga innan man röstat.")),
        (AFTER, _("Gör resultaten synliga efter att man röstat.")),
        (ON_CLOSE, _("Gör resultaten synliga när röstningen stängt.")),
    )
    verification = models.CharField(
        verbose_name=_('verifiering'),
        max_length=255,
        help_text=_("Verifieringskod att ange vid omröstningen, valfritt."),
        blank=True,
        null=True
    )
    question_group = models.ForeignKey(QuestionGroup, verbose_name=_('frågegrupp'),)
    name = models.CharField(verbose_name=_('fråga'), max_length=255)
    body = models.TextField(verbose_name=_("utförlig information"),
                            help_text=_("Utförligare information till frågan."),
                            blank=True,
                            null=True,)
    result = models.CharField(
        max_length=1,
        choices=RESULT,
        default=PRIVATE,
        blank=False,
        null=False,
        verbose_name=_("resultattyp")
    )
    publish_results = models.CharField(
        max_length=1,
        choices=PUBLISH_RESULT_OPTIONS,
        default=ON_CLOSE,
        blank=False,
        null=False,
        verbose_name=_("publicerings alternativ"))
    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=DRAFT,
        blank=False,
        null=False,
        help_text=_("Kan inte ändras tillbaka till draft efter att det öppnats"
                    " och kan inte öppnats efter att den stängts. "
                    "Det går inte heller att göra ändringar på annat än status och "
                    "verifieringskod efter att draft läget lämnats.")
    )
    nr_of_picks = models.IntegerField(verbose_name=_("Max antal val en användare kan kryssa i på frågan."), default=1)
    min_nr_of_picks = models.IntegerField(
        verbose_name=_("Min antal val en användare kan kryssa i på frågan."), default=0)
    anonymous = models.BooleanField(verbose_name=_('anonym'), default=True)
    result_readers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("användare som kan se resultatet"),
        help_text=_("Användaren som kan se resultatet i omröstningen, används bara om resultattypen är: "
                    "\"Privat åtkomst enbart för personer listade i \"Användare som kan se resultatet\"\" "),
        related_name="result_reader",
        blank=True
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("användare"),
        help_text=_("Användaren som ändrat på frågan."),
        null=True,
        on_delete=models.SET_NULL)

    objects = QuestionManager()

    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)
        self._initial_status = self.status

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
            return self.question_group.event.entryasparticipant_set.values_list('user', flat=True)
        elif self.question_group.question_status == QuestionGroup.ALL:
            return settings.AUTH_USER_MODEL.objects.all()

    def is_voter(self, user):
        return self.voters().filter(user=user).exists()

    def has_voted(self, user):
        return self.hasvoted_set.filter(user=user).exists()

    def can_vote(self, user):
        return self.is_voter(user) and not self.has_voted(user) and self.status == self.OPEN

    def _internal_timing_of_result(self, user):
        if self.publish_results == Question.ON_CLOSE:
            if self.status == Question.CLOSED:
                return True
            else:
                return False
        elif self.publish_results == Question.BEFORE:
            return True
        elif self.publish_results == Question.AFTER:
            if self.has_voted(user):
                return True
            else:
                return False
        else:
            return False

    def _internal_result_status(self, user):
        if self.result == Question.PUBLIC_DETAILED or self.result == Question.PUBLIC_LIMITED:
            return True
        elif self.result == Question.PRIVATE and self.question_group.can_administer(user):
            return True
        elif self.result == Question.SUPER_PRIVATE and user in self.result_readers.all():
            return True
        else:
            return False

    def show_result(self, user):
        if self._internal_result_status(user):
            return self._internal_timing_of_result(user)
        else:
            return False

    def detailed(self, user):
        if self.result == Question.PUBLIC_LIMITED and not self.question_group.can_administer(user):
            return False
        else:
            return True

    def get_result(self):
        voters = self.voters().count()
        has_voted = self.hasvoted_set.all().count()
        result = list(self.vote_set.all().values('option__name').annotate(total=Count('option')).order_by('-total'))
        nr_of_votes = self.vote_set.all().count()
        place = 1
        iteration = 1
        tmp = 0
        for r in result:
            if tmp != r['total']:
                place = iteration
            r['place'] = place
            tmp = r['total']
            iteration += 1
        return {
            "voters": voters,
            "has_voted": has_voted,
            "result": result,
            "attendance": "{percent}%".format(percent=(has_voted/voters)*100),
            "nr_of_votes": nr_of_votes,
            "nr_of_blanks": ((self.nr_of_picks*has_voted)-nr_of_votes)
        }

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
        if len(options) < self.min_nr_of_picks:
            raise CouldNotVoteException(reason=_("Du har valt för få alternativ."))
        for option in options:
            Vote.objects.create(question=self, option_id=option, user=user)
        HasVoted.objects.create(question=self, user=user)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            if self.status == Question.DRAFT and self._initial_status != Question.DRAFT:
                self.status = self._initial_status
            elif self.status == Question.OPEN and self._initial_status == Question.CLOSED:
                self.status = self._initial_status
        super(Question, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


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
