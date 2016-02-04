from django.db import models
from django.utils import timezone


class ArticleManager(models.Manager):

    def published(self):
        return self.filter(
            status=self.model.APPROVED,
            visible_from__lte=timezone.now(),
            visible_to__gte=timezone.now()
            ).order_by('-visible_from')
