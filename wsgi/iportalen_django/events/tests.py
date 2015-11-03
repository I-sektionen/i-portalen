
from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from user_managements.models import IUser
from .models import Event


class EventTests(TestCase):
    def setUp(self):
        creator = IUser.objects.create_user(username="testa123")
        random_guy = IUser.objects.create_user(username="testa321")
        creator_pall = IUser.objects.create_user(username="liuid123")

        info = IUser.objects.create_user(username="liuid666")
        perm = Permission.objects.get(codename="can_approve_event")
        info.user_permissions.add(perm)
        info.save()

        e = Event.objects.create(user=creator,
                                 headline="Eventheader",
                                 lead="Eventlead",
                                 body="Eventbody",
                                 location="C1",
                                 start="2015-11-04 15:34",
                                 end="2015-11-04 16:56",
                                 visible_from="2014-11-04 15:34",
                                 enable_registration=True,
                                 registration_limit=2)

    def test_approve_event(self):
        event = Event.objects.get(headline__exact='Eventheader')
        random_guy = IUser.objects.get(username="testa321")
        info = IUser.objects.get(username="liuid666")
        creator = IUser.objects.get(username="testa123")

        self.assertEqual(event.status, Event.DRAFT)

        self.assertFalse(event.send_to_approval(random_guy))

        event.send_to_approval(creator)
        self.assertEqual(event.status, Event.BEING_REVIEWED)

        msg = "You suck!"
        event.reject(info, msg=msg)

        self.assertEqual(event.status, Event.REJECTED)
        self.assertEqual(event.rejection_message, msg)

        event.send_to_approval(creator)

        event.approve(info)
        self.assertEqual(event.status, Event.APPROVED)

        event2 = Event.objects.get(headline__exact='Eventheader')
        self.assertEqual(event2.status, Event.APPROVED)
        self.assertEqual(event2.rejection_message, event.rejection_message)

#TODO: Test registration periods. Reserve lists, deregistration, edit form access rights.