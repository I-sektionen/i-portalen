from django.db import models
from django.utils import timezone


class AlumniManager(models.Manager):

    def published(self):
        return self.filter(
            visible_from__lte=timezone.now(),
            visible_to__gte=timezone.now()
            ).order_by('-visible_from')

    def user(self, user):
        user_articles = user.article_set.filter(visible_to__gte=timezone.now()).order_by('-visible_from')
        user_org = user.get_organisations()

        for o in user_org:
            user_articles |= o.article_set.filter(visible_to__gte=timezone.now()).order_by('-visible_from')
        return user_articles
