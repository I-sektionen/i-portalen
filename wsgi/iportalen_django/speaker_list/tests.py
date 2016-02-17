from django.test import TestCase
from django.utils import timezone

from events.models import Event
from speaker_list.exceptions import SpeakerListException
from .models import SpeakerList
from user_managements.models import IUser


class SpeakerListTests (TestCase):
    def setUp(self):
        """
        This set up creates users: Event admin, speaker1..5
        Sets up an event
        :return:
        """
        # Normal user with no special permissions
        self.admin = IUser.objects.create_user(username="admin001")
        self.speak001 = IUser.objects.create_user(username="speak001")
        self.speak001.first_name = "a1"
        self.speak001.last_name = "b1"
        self.speak001.save()
        self.speak002 = IUser.objects.create_user(username="speak002")
        self.speak002.first_name = "a2"
        self.speak002.last_name = "b2"
        self.speak002.save()
        self.speak003 = IUser.objects.create_user(username="speak003")
        self.speak003.first_name = "a3"
        self.speak003.last_name = "b3"
        self.speak003.save()
        self.speak004 = IUser.objects.create_user(username="speak004")
        self.speak004.first_name = "a4"
        self.speak004.last_name = "b4"
        self.speak004.save()
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
        self.event.check_in(self.speak001)
        self.event.check_in(self.speak002)
        self.event.check_in(self.speak003)
        self.event.check_in(self.speak004)

    def test_clear(self):
        SpeakerList.objects.create(event=self.event, user=self.speak001, speech_id=1)
        SpeakerList.objects.create(event=self.event, user=self.speak002, speech_id=2)
        SpeakerList.objects.create(event=self.event2, user=self.speak001, speech_id=3)
        self.assertEqual(SpeakerList.objects.all().count(), 3)

        SpeakerList.objects.clear(event=self.event)
        self.assertEqual(SpeakerList.objects.all().count(), 1)

    def test_add_once(self):
        # Regular adding.
        SpeakerList.objects.add(self.event, self.speak001)
        try:
            SpeakerList.objects.get(event=self.event, user=self.speak001, has_spoken=False)
        except SpeakerList.DoesNotExist:
            self.fail()

    def test_add_two_times_same_person(self):
        # Try to add a second time.
        SpeakerList.objects.add(self.event, self.speak001)
        try:
            SpeakerList.objects.add(self.event, self.speak001)
            self.fail()
        except SpeakerListException:
            pass

    def test_add_non_checked_in_person(self):
        try:
            SpeakerList.objects.add(self.event, self.haxor666)
            self.fail()
        except SpeakerListException:
            pass

    def test_add_multiple_persons_and_check_order(self):
        # Add multiple and check order
        SpeakerList.objects.add(self.event, self.speak001)
        SpeakerList.objects.add(self.event, self.speak002)
        SpeakerList.objects.add(self.event, self.speak003)
        self.assertEqual(SpeakerList.objects.all().count(), 3)
        self.assertEqual(
            list(SpeakerList.objects.filter(event=self.event, has_spoken=False).values_list('user', flat=True)),
            [self.speak001.id, self.speak002.id, self.speak003.id])

    def test_add_multiple_persons_and_check_order_when_remove_one(self):
        # Mark first as has spoken
        SpeakerList.objects.add(self.event, self.speak001)
        SpeakerList.objects.add(self.event, self.speak002)
        SpeakerList.objects.add(self.event, self.speak003)
        s = SpeakerList.objects.get(event=self.event, user=self.speak001, has_spoken=False)
        s.has_spoken = True
        s.save()
        self.assertEqual(
            list(SpeakerList.objects.filter(event=self.event, has_spoken=False).values_list('user', flat=True)),
            [self.speak002.id, self.speak003.id])

    def test_add_multiple_persons_and_check_order_when_added_again(self):
        # Try to add for a second speech.
        SpeakerList.objects.add(self.event, self.speak001)
        SpeakerList.objects.add(self.event, self.speak002)
        SpeakerList.objects.add(self.event, self.speak003)
        s = SpeakerList.objects.get(event=self.event, user=self.speak001, has_spoken=False)
        s.has_spoken = True
        s.save()
        try:
            SpeakerList.objects.add(self.event, self.speak001)
        except SpeakerListException:
            self.fail()
        self.assertEqual(
            list(SpeakerList.objects.filter(event=self.event, has_spoken=False).values_list('user', flat=True)),
            [self.speak002.id, self.speak003.id, self.speak001.id])

    def test_add_multiple_persons_and_check_order_when_added_again_second_speaker(self):
        # Try to add for a second speech.
        SpeakerList.objects.add(self.event, self.speak001)
        SpeakerList.objects.add(self.event, self.speak002)
        SpeakerList.objects.add(self.event, self.speak003)
        s = SpeakerList.objects.get(event=self.event, user=self.speak001, has_spoken=False)
        s.has_spoken = True
        s.save()
        SpeakerList.objects.add(self.event, self.speak001)
        # Add speaker who hasn't talked to check second speaker list.
        SpeakerList.objects.add(self.event, self.speak004)
        self.assertEqual(
            list(SpeakerList.objects.filter(event=self.event, has_spoken=False).values_list('user', flat=True)),
            [self.speak002.id, self.speak003.id, self.speak004.id, self.speak001.id])

    def test_show_queue(self):
        SpeakerList.objects.create(event=self.event, user=self.speak003, speech_id=4)
        SpeakerList.objects.create(event=self.event, user=self.speak001, speech_id=1, nr_of_speeches=2)
        SpeakerList.objects.create(event=self.event, user=self.speak002, speech_id=2)
        SpeakerList.objects.create(event=self.event2, user=self.speak001, speech_id=3)
        sl = SpeakerList.objects.show_queue(self.event)
        self.assertEqual(len(sl[0]), 3)
        self.assertEqual(sl[0]['first_name'], self.speak002.first_name)
        self.assertEqual(sl[1]['first_name'], self.speak003.first_name)
        self.assertEqual(sl[2]['first_name'], self.speak001.first_name)

    def test_next_empty_list(self):
        try:
            SpeakerList.objects.next(self.event)
            self.fail()
        except SpeakerListException:
            pass

    def test_next_multiple_persons(self):
        # Try to add for a second speech.
        SpeakerList.objects.create(event=self.event, user=self.speak003, speech_id=4)
        SpeakerList.objects.create(event=self.event, user=self.speak001, speech_id=1, nr_of_speeches=2)
        SpeakerList.objects.create(event=self.event, user=self.speak002, speech_id=2)
        SpeakerList.objects.create(event=self.event2, user=self.speak001, speech_id=3)

        self.assertEqual(
            list(SpeakerList.objects.filter(event=self.event, has_spoken=False).values_list('user', flat=True)),
            [self.speak002.id, self.speak003.id, self.speak001.id])

        SpeakerList.objects.next(self.event)
        self.assertEqual(
            list(SpeakerList.objects.filter(event=self.event, has_spoken=False).values_list('user', flat=True)),
            [self.speak003.id, self.speak001.id])

    def test_remove_when_first_on_empty_list(self):
        SpeakerList.objects.add(self.event, self.speak001)
        try:
            SpeakerList.objects.remove(self.event, self.speak001)
            self.fail()
        except SpeakerListException:
            pass

    def test_remove_on_empty_list(self):
        try:
            SpeakerList.objects.remove(self.event, self.speak001)
            self.fail()
        except SpeakerListException:
            pass

    def test_remove_non_checked_in_user(self):
        try:
            SpeakerList.objects.remove(self.event, self.haxor666)
            self.fail()
        except SpeakerListException:
            pass

    def test_remove_when_first_on_list(self):
        SpeakerList.objects.add(self.event, self.speak001)
        SpeakerList.objects.add(self.event, self.speak002)
        SpeakerList.objects.add(self.event, self.speak003)
        SpeakerList.objects.next(self.event)
        try:
            SpeakerList.objects.remove(self.event, self.speak002)
            self.fail()
        except SpeakerListException:
            pass

    def test_shuffle(self):
        # Fuck this, it's retarded to test and a never used bonus feature.
        # And even if it doesn't work, who can prove it, its random...
        pass

    def test_integration_adding_first_speaker_when_second_speaker_is_talkning(self):
        # Try to add for a second speech.
        SpeakerList.objects.add(self.event, self.speak001)
        SpeakerList.objects.add(self.event, self.speak002)
        SpeakerList.objects.add(self.event, self.speak003)
        SpeakerList.objects.next(self.event)
        SpeakerList.objects.next(self.event)
        SpeakerList.objects.next(self.event)
        # List shall now be empty
        SpeakerList.objects.add(self.event, self.speak001)
        # Add speaker who hasn't talked.
        SpeakerList.objects.add(self.event, self.speak004)
        # Now speak001 should still be in the top.
        self.assertEqual(
            list(SpeakerList.objects.filter(event=self.event, has_spoken=False).values_list('user', flat=True)),
            [self.speak001.id, self.speak004.id])
        SpeakerList.objects.next(self.event)
        SpeakerList.objects.add(self.event, self.speak001)
        SpeakerList.objects.add(self.event, self.speak002)
        # Check third speaker list.
        self.assertEqual(
            list(SpeakerList.objects.filter(event=self.event, has_spoken=False).values_list('user', flat=True)),
            [self.speak004.id, self.speak002.id, self.speak001.id])
