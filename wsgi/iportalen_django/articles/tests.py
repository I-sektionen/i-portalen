from django.utils import timezone

from django.test import TestCase
from django.contrib.auth.models import Group, Permission, AnonymousUser

from articles.models import Article
from organisations.models import Organisation
from user_managements.models import IUser


class ArticleTests (TestCase):
    def setUp(self):
        """
        This set up creates users: Author, group member, normal user, content approver, superuser.
        :return:
        """
        # Normal user with no special permissions
        nrml_user = IUser.objects.create_user(username="norus111")

        # Super user with all permissions
        super_user = IUser.objects.create_superuser(username="supus111", password="123")

        #InfO or other person with permission to aprove content
        content_approver = IUser.objects.create_user(username="conap111")
        content_approver_group, created = Group.objects.get_or_create(name='approvers')
        perm = Permission.objects.get(codename='can_approve_article')
        content_approver_group.permissions.add(perm)
        content_approver_group.user_set.add(content_approver)

        # Auther of article and a user in same group as author.
        author = IUser.objects.create_user(username="autho111")
        group_member = IUser.objects.create_user(username="grpme111")
        authors_group, created = Group.objects.get_or_create(name='authors_group')
        authors_group.user_set.add(group_member)
        authors_group.user_set.add(author)
        organisation = Organisation.objects.create(name="org", group=authors_group)

    def _get_users(self):
        return {
            "normal_user": IUser.objects.get(username="norus111"),
            "super_user": IUser.objects.get(username="supus111"),
            "content_approver": IUser.objects.get(username="conap111"),
            "author": IUser.objects.get(username="autho111"),
            "group_member": IUser.objects.get(username="grpme111"),
            "authors_group": Group.objects.get(name='authors_group'),
            "authors_org": Organisation.objects.get(name="org")
        }

    def _create_an_article(self, author=None, unpublish_time=None, publish_time=None):
        if author is None:
            author = IUser.objects.get(username="autho111")

        if unpublish_time is None:
            unpublish_time = timezone.now() + timezone.timedelta(days=35)
        if publish_time is None:
            publish_time = timezone.now() - timezone.timedelta(days=1)
        org = Organisation.objects.get(name="org")
        a = Article(headline="headline",
                    lead="a short lead",
                    body="an even shorter boyd",
                    visible_from=publish_time,
                    visible_to=unpublish_time,
                    user=author,
                    )
        a.save()  # Must save before m2m add...?
        a.organisations.add(org)
        a.save()
        return a

    def test_create_an_article(self):
        """
        This tests creates an article and verifies that it is existing. Then it checks publishing.
        :return:
        """
        u_dict = self._get_users()
        a = self._create_an_article(u_dict["author"])
        a2 = Article.objects.get(headline="headline")
        self.assertEqual(a.headline, a2.headline)

    def test_can_approve(self):
        u_dict = self._get_users()
        a = self._create_an_article(u_dict["author"])
        self.assertEqual(a.status, Article.DRAFT)

        self.assertFalse(a.approve(u_dict["content_approver"]))
        self.assertEqual(a.status, Article.DRAFT)
        self.assertFalse(a.approve(u_dict["author"]))
        self.assertEqual(a.status, Article.DRAFT)
        self.assertFalse(a.approve(u_dict["normal_user"]))
        self.assertEqual(a.status, Article.DRAFT)

        a.status = Article.BEING_REVIEWED
        self.assertFalse(a.approve(u_dict["normal_user"]))
        self.assertEqual(a.status, Article.BEING_REVIEWED)
        self.assertFalse(a.approve(u_dict["author"]))
        self.assertEqual(a.status, Article.BEING_REVIEWED)
        self.assertTrue(a.approve(u_dict["content_approver"]))
        self.assertEqual(a.status, Article.APPROVED)

    def test_can_administer(self):
        u_dict = self._get_users()
        a = self._create_an_article(u_dict["author"])
        self.assertFalse(a.can_administer(u_dict["normal_user"]))
        self.assertFalse(a.can_administer(AnonymousUser()))
        self.assertTrue(a.can_administer(u_dict["author"]))
        self.assertTrue(a.can_administer(u_dict["group_member"]))
        self.assertTrue(a.can_administer(u_dict["super_user"]))
        self.assertTrue(a.can_administer(u_dict["content_approver"]))

    def test_publish_times(self):
        u_dict = self._get_users()
        a = self._create_an_article()

        self.assertTrue(a.show_article_before_experation)

        a2 = self._create_an_article(publish_time=timezone.now() - timezone.timedelta(days=2),
                                     unpublish_time=timezone.now() - timezone.timedelta(days=1))  # Publish in two days
        self.assertTrue(a.show_article_before_experation)

#  TODO: Test Article.approve()
#  TODO: Test Article.reject()
#  TODO: Test Article.get_new_status()  wtf...
