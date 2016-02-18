from django.test import TestCase
from django.utils import timezone

from events.models import Event

from user_managements.models import IUser
from votings.exceptions import CouldNotVoteException
from votings.models import QuestionGroup, Question, HasVoted, Option


class VotingTests (TestCase):
    def setUp(self):
        """
        This set up creates users: Event admin, voterer1..5
        Sets up an event
        """
        # Normal user with no special permissions
        self.admin = IUser.objects.create_user(username="admin001")
        self.voter001 = IUser.objects.create_user(username="voter001")
        self.voter001.first_name = "a1"
        self.voter001.last_name = "b1"
        self.voter001.save()
        self.voter002 = IUser.objects.create_user(username="voter002")
        self.voter002.first_name = "a2"
        self.voter002.last_name = "b2"
        self.voter002.save()
        self.voter003 = IUser.objects.create_user(username="voter003")
        self.voter003.first_name = "a3"
        self.voter003.last_name = "b3"
        self.voter003.save()
        self.voter004 = IUser.objects.create_user(username="voter004")
        self.voter004.first_name = "a4"
        self.voter004.last_name = "b4"
        self.voter004.save()
        self.haxor666 = IUser.objects.create_user(username="haxor666")
        self.haxor666.first_name = "a5"
        self.haxor666.last_name = "b5"
        self.haxor666.save()
        self.event = Event.objects.create(
            headline="test event",
            lead="test event",
            body="test event",
            location="test event",
            start=timezone.now(),
            end=timezone.now()+timezone.timedelta(hours=4),
            enable_registration=True,
            registration_limit=5,
            visible_from=timezone.now()-timezone.timedelta(hours=4),
            user=self.admin,
            status=Event.APPROVED
        )
        self.event2 = Event.objects.create(
            headline="test event2",
            lead="test event2",
            body="test event2",
            location="test event2",
            start=timezone.now(),
            end=timezone.now()+timezone.timedelta(hours=4),
            enable_registration=True,
            registration_limit=5,
            visible_from=timezone.now()-timezone.timedelta(hours=4),
            user=self.admin,
            status=Event.APPROVED
        )
        self.event.check_in(self.voter001)
        self.event.check_in(self.voter002)
        self.event.check_in(self.voter003)
        self.event.check_in(self.voter004)
        self.qg = QuestionGroup.objects.create(name=self.event.headline,
                                               question_status=QuestionGroup.EVENT,
                                               event=self.event,
                                               creator=self.admin,
                                               visible_from=timezone.now()-timezone.timedelta(hours=4),
                                               visible_to=timezone.now()+timezone.timedelta(hours=4),)

    def test_QG_published(self):
        self.assertEqual(QuestionGroup.objects.published().count(), 1)
        self.qg.visible_to = timezone.now()-timezone.timedelta(hours=2)
        self.qg.save()
        self.assertEqual(QuestionGroup.objects.published().count(), 0)
        self.qg.visible_to = timezone.now()+timezone.timedelta(hours=2)
        self.qg.visible_from = timezone.now()+timezone.timedelta(hours=2)
        self.qg.save()
        self.assertEqual(QuestionGroup.objects.published().count(), 0)
        self.qg.visible_to = timezone.now()+timezone.timedelta(hours=4)
        self.qg.visible_from = timezone.now()-timezone.timedelta(hours=4)
        self.qg.save()
        self.assertEqual(QuestionGroup.objects.published().count(), 1)

    def test_Q_published(self):
        q = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin)
        self.assertEqual(Question.objects.published().count(), 0)

        q.status = Question.OPEN
        q.save()
        self.assertEqual(Question.objects.published().count(), 1)

    def test_QG_can_administer(self):
        self.assertTrue(self.qg.can_administer(self.admin))
        self.assertFalse(self.qg.can_administer(self.haxor666))
        self.assertFalse(self.qg.can_administer(self.voter001))

    def test_voters(self):
        q = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin)
        self.assertEqual(q.voters().count(), 4)
        self.assertTrue(self.voter001.pk in q.voters())
        self.assertFalse(self.haxor666.pk in q.voters())

    def test_is_voter(self):
        q = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin)
        self.assertTrue(q.is_voter(self.voter001))
        self.assertTrue(q.is_voter(self.voter002))
        self.assertFalse(q.is_voter(self.haxor666))

    def test_has_voted(self):
        q = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.OPEN
        )
        self.assertFalse(q.has_voted(self.voter001))
        HasVoted.objects.create(question=q, user=self.voter001)
        self.assertTrue(q.has_voted(self.voter001))
        self.assertFalse(q.has_voted(self.haxor666))
        q2 = Question.objects.create(
            question_group=self.qg,
            name="Why2?",
            body="Well, why2?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.OPEN)
        self.assertTrue(q.has_voted(self.voter001))
        self.assertFalse(q2.has_voted(self.voter001))

    def test_can_vote(self):
        q1 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.OPEN
        )
        q2 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.DRAFT
        )
        q3 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.CLOSED
        )
        self.assertTrue(q1.can_vote(self.voter001))
        self.assertFalse(q1.can_vote(self.haxor666))
        HasVoted.objects.create(question=q1, user=self.voter001)
        self.assertFalse(q1.can_vote(self.voter001))
        self.assertFalse(q2.can_vote(self.voter001))
        self.assertFalse(q3.can_vote(self.voter001))

    def test_internal_timing_of_result(self):
        q1 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.CLOSED,
            publish_results=Question.ON_CLOSE
        )
        self.assertTrue(q1._internal_timing_of_result(self.voter001))
        q2 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.OPEN,
            publish_results=Question.ON_CLOSE
        )
        self.assertFalse(q2._internal_timing_of_result(self.voter001))
        q3 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.OPEN,
            publish_results=Question.BEFORE
        )
        self.assertTrue(q3._internal_timing_of_result(self.voter001))
        q4 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.OPEN,
            publish_results=Question.AFTER
        )
        self.assertFalse(q4._internal_timing_of_result(self.voter001))
        HasVoted.objects.create(question=q4, user=self.voter001)
        self.assertTrue(q4._internal_timing_of_result(self.voter001))

    def test_internal_result_status(self):
        q0 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.CLOSED,
            result=Question.PUBLIC_DETAILED,
            publish_results=Question.ON_CLOSE
        )
        self.assertTrue(q0._internal_result_status(self.voter001))
        q1 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.CLOSED,
            result=Question.PUBLIC_LIMITED,
            publish_results=Question.ON_CLOSE
        )
        self.assertTrue(q1._internal_result_status(self.voter001))
        q2 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.CLOSED,
            result=Question.PRIVATE,
            publish_results=Question.ON_CLOSE
        )
        self.assertFalse(q2._internal_result_status(self.voter001))
        self.assertTrue(q2._internal_result_status(self.admin))
        q3 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.CLOSED,
            result=Question.SUPER_PRIVATE,
            publish_results=Question.ON_CLOSE,
        )
        q3.result_readers.add(self.voter002)
        q3.result_readers.add(self.voter003)
        self.assertFalse(q3._internal_result_status(self.voter001))
        self.assertFalse(q3._internal_result_status(self.admin))
        self.assertFalse(q3._internal_result_status(self.haxor666))
        self.assertTrue(q3._internal_result_status(self.voter002))
        self.assertTrue(q3._internal_result_status(self.voter003))

    def test_detailed(self):
        q1 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.CLOSED,
            result=Question.PUBLIC_LIMITED,
            publish_results=Question.ON_CLOSE
        )
        self.assertFalse(q1.detailed(self.voter001))
        self.assertTrue(q1.detailed(self.admin))

    def test_vote(self):
        q1 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=1,
            modified_by=self.admin,
            status=Question.OPEN,
        )
        o1 = Option.objects.create(name="svar1", question=q1)
        o2 = Option.objects.create(name="svar2", question=q1)
        try:
            q1.vote(self.voter001, [o1.pk])
        except CouldNotVoteException:
            self.fail()
        try:
            q1.vote(self.voter001, [o2.pk])
            self.fail()
        except CouldNotVoteException:
            pass
        try:
            q1.vote(self.haxor666, [o1.pk])
            self.fail()
        except CouldNotVoteException:
            pass
        try:
            q1.vote(self.voter003, [])
        except CouldNotVoteException:
            self.fail()
        # Closig question
        q1.status = Question.CLOSED
        q1.save()
        try:
            q1.vote(self.voter002, [o1.pk])
            self.fail()
        except CouldNotVoteException:
            pass

        q2 = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=3,
            min_nr_of_picks=2,
            modified_by=self.admin,
            status=Question.OPEN,
        )
        o1 = Option.objects.create(name="svar1", question=q2)
        o2 = Option.objects.create(name="svar2", question=q2)
        o3 = Option.objects.create(name="svar3", question=q2)
        o4 = Option.objects.create(name="svar4", question=q2)
        try:
            q2.vote(self.voter001, [o1.pk])
            self.fail()
        except CouldNotVoteException:
            pass
        try:
            q2.vote(self.voter001, [o1.pk, o2.pk])
        except CouldNotVoteException:
            self.fail()
        try:
            q2.vote(self.voter002, [o1.pk, o2.pk, o3.pk, o4.pk])
            self.fail()
        except CouldNotVoteException:
            pass
        try:
            q2.vote(self.voter002, [o1.pk, o2.pk, o3.pk])
        except CouldNotVoteException:
            self.fail()

    def save_voting(self):
        q = Question.objects.create(
            question_group=self.qg,
            name="Why?",
            body="Well, why?",
            nr_of_picks=3,
            min_nr_of_picks=2,
            modified_by=self.admin,
            status=Question.DRAFT,
        )
        q.status = Question.OPEN
        q.save()
        self.assertEqual(Question.OPEN, q.status)
        q.status = Question.DRAFT
        q.save()
        self.assertEqual(Question.OPEN, q.status)
        q.status = Question.CLOSED
        q.save()
        self.assertEqual(Question.CLOSED, q.status)
        q.status = Question.OPEN
        q.save()
        self.assertEqual(Question.CLOSED, q.status)
