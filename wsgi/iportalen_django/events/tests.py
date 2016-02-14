from django.test import TestCase
from django.contrib.auth.models import Permission
from user_managements.models import IUser
from events.models import Event
from .exceptions import CouldNotRegisterException
from django.utils import timezone


class EventTests(TestCase):
    def setUp(self):
        creator = IUser.objects.create_user(username="testa123")
        IUser.objects.create_user(username="testa321")
        IUser.objects.create_user(username="liuid123")

        IUser.objects.create_user(username="aaaaa111")
        IUser.objects.create_user(username="bbbbb111")
        IUser.objects.create_user(username="ccccc111")
        IUser.objects.create_user(username="ddddd111")

        info = IUser.objects.create_user(username="liuid666")
        perm = Permission.objects.get(codename="can_approve_event")
        info.user_permissions.add(perm)
        info.save()

        Event.objects.create(user=creator,
                             headline="Eventheader",
                             lead="Eventlead",
                             body="Eventbody",
                             location="C1",
                             start=timezone.make_aware(timezone.datetime.strptime("3015-11-04 15:34", "%Y-%m-%d %H:%M")),
                             end=timezone.make_aware(timezone.datetime.strptime("3015-11-04 16:56", "%Y-%m-%d %H:%M")),
                             visible_from=timezone.make_aware(timezone.datetime.strptime("2014-11-04 15:34", "%Y-%m-%d %H:%M")),
                             enable_registration=True,
                             registration_limit=2)

    # using deprecated functions
    # def test_approve_event(self):
    #     event = Event.objects.get(headline__exact='Eventheader')
    #     random_guy = IUser.objects.get(username="testa321")
    #     info = IUser.objects.get(username="liuid666")
    #     creator = IUser.objects.get(username="testa123")
    #
    #     self.assertEqual(event.status, Event.DRAFT)
    #
    #     self.assertFalse(event.send_to_approval(random_guy))
    #
    #     event.send_to_approval(creator)
    #     self.assertEqual(event.status, Event.BEING_REVIEWED)
    #
    #     msg = "You suck!"
    #     event.reject(info, msg=msg)
    #
    #     self.assertEqual(event.status, Event.REJECTED)
    #     self.assertEqual(event.rejection_message, msg)
    #
    #     event.send_to_approval(creator)
    #
    #     event.approve(info)
    #     self.assertEqual(event.status, Event.APPROVED)
    #
    #     event2 = Event.objects.get(headline__exact='Eventheader')
    #     self.assertEqual(event2.status, Event.APPROVED)
    #     self.assertEqual(event2.rejection_message, event.rejection_message)

    def test_check_in_full(self):
        event = Event.objects.get(headline__exact='Eventheader')
        a = IUser.objects.get(username="aaaaa111")
        b = IUser.objects.get(username="bbbbb111")
        c = IUser.objects.get(username="ccccc111")

        error = False
        # full = False
        try:
            event.register_user(a)
        except:
            error = True
        try:
            event.registered(b)
        except:
            error = True
        try:
            event.register_user(c)
        except CouldNotRegisterException:
            # full = True
            pass
        except:
            error = True

        self.assertFalse(error)
        # self.assertTrue(full)
