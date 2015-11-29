from django.utils import timezone

from django.test import TestCase

from .models import Article
from user_managements.models import IUser


class ArticleTests (TestCase):
    def test_create_an_article(self):
        """
        This tests creates an article and verifies that it is existing. Then it checks publishing.
        :return:
        """
        u = IUser.objects.create_user(username="isaek808")
        publish_time = timezone.now() + timezone.timedelta(days=30)
        unpublish_time = timezone.now() + timezone.timedelta(days=35)
        a = Article(headline="headline",
                    lead="a short lead",
                    body="an even shorter boyd",
                    visible_from=publish_time,
                    visible_to=unpublish_time,
                    approved=False,
                    user=u,
                    )

        self.assertEqual(a.headline, "headline")
        self.assertFalse(a.approved)



