__author__ = 'jonathan'
from django.db import models
from django.utils import timezone

class ArticleManager(models.Manager):
    def get_user_articles(self, user):
        approved_articles = user.article_set.filter(approved=True, visible_to__gte=timezone.now())
        unapproved_articles = user.article_set.filter(approved=False, draft=False, visible_to__gte=timezone.now())
        draft_articles = user.article_set.filter(draft=True, visible_to__gte=timezone.now())

        return {'approved_articles':approved_articles, 'unapproved_articles':unapproved_articles, 'draft_articles':draft_articles}