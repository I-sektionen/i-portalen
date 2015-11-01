from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from user_managements.models import IUser
from .models import Event

class EventTests(TestCase):
    def setUp(self):
        author = IUser.objects.create_user(username="testa123")
        member = IUser.objects.create_user(username="testa321")
        not_member = IUser.objects.create_user(username="liuid123")
        info = IUser.objects.create_user(username="liuid666")
        info.save()

        e = Event.objects.create(name="Eventnamn")
        e.headline = "Eventheader"
        e.lead = "Eventlead"
        e.body = "Eventbody"
        e.location = "C1"

        e.start = "2015-11-04 15:34"
        e.end = "2015-11-04 16:56"

        e.enable_registration = "true"
        e.registration_limit = 2


        e.save()

    #def test_create_event(self):

    #def test_registration_limit(self):

