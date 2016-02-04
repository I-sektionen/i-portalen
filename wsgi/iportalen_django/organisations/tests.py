from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from user_managements.models import IUser
from organisations.models import Organisation


class OrganisationTests(TestCase):
    def setUp(self):
        leader = IUser.objects.create_user(username="testa123")
        member = IUser.objects.create_user(username="testa321")

        info = IUser.objects.create_user(username="liuid666")
        perm = Permission.objects.get(codename="change_organisation")
        info.user_permissions.add(perm)
        info.save()

        g = Group.objects.create(name="org_group")
        g.user_set.add(leader)
        g.user_set.add(member)

        o = Organisation.objects.create(name="Organisations namn")
        o.leader = leader
        o.group = g
        o.save()

    def test_create_organization(self):
        leader = IUser.objects.get(username__exact="testa123")
        group = Group.objects.get(name__exact="org_group")
        org = Organisation.objects.get(name__exact="Organisations namn")

        self.assertEqual("Organisations namn", org.name)
        self.assertEqual(group, org.group)
        self.assertEqual(leader, org.leader)

    def test_edit_organisations(self):
        org = Organisation.objects.get(name__exact="Organisations namn")
        leader = IUser.objects.get(username__exact="testa123")
        member = IUser.objects.get(username__exact="testa321")
        non_member = IUser.objects.get(username__exact="liuid123")

        self.assertFalse(org.can_edit(member))
        self.assertFalse(org.can_edit(non_member))
        self.assertTrue(org.can_edit(leader))
