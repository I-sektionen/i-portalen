from django.db import models
from django.utils import timezone
from articles.models import APPROVED, BEING_REVIEWED, DRAFT, REJECTED


class ArticleManager(models.Manager):

    def get_user_articles(self, user):
        """Get article's writen by a user"""
        approved_articles = user.article_set.filter(status=APPROVED, visible_to__gte=timezone.now())
        unapproved_articles = user.article_set.filter(status=BEING_REVIEWED, visible_to__gte=timezone.now())
        draft_articles = user.article_set.filter(status=DRAFT, visible_to__gte=timezone.now())
        rejected_articles = user.article_set.filter(status=REJECTED, visible_to__gte=timezone.now())

        return {'approved_articles': approved_articles, 'unapproved_articles': unapproved_articles,
                'draft_articles': draft_articles, 'rejected_articles': rejected_articles}
