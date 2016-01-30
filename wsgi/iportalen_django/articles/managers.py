from django.db import models
from django.utils import timezone


class ArticleManager(models.Manager):

    def published(self):
        return self.filter(
            status=self.model.APPROVED,
            visible_from__lte=timezone.now(),
            visible_to__gte=timezone.now()
            ).order_by('-visible_from')

    # def get_user_articles(self, user):
    #     """Get article's writen by a user"""
    #     approved_articles = user.article_set.filter(status=self.model.APPROVED, visible_to__gte=timezone.now())
    #     unapproved_articles = user.article_set.filter(status=self.model.BEING_REVIEWED, visible_to__gte=timezone.now())
    #     draft_articles = user.article_set.filter(status=self.model.DRAFT, visible_to__gte=timezone.now())
    #     rejected_articles = user.article_set.filter(status=self.model.REJECTED, visible_to__gte=timezone.now())
    #
    #     return {'approved_articles': approved_articles, 'unapproved_articles': unapproved_articles,
    #             'draft_articles': draft_articles, 'rejected_articles': rejected_articles}
