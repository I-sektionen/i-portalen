from django.db import models
from django.utils import timezone


class QuestionGroupManager(models.Manager):
    def published(self):
        return self.filter(
                visible_from__lte=timezone.now(),
                visible_to__gte=timezone.now()
                ).order_by('-pk')


class QuestionManager(models.Manager):
    def published(self):
        return self.filter(
                status=self.model.OPEN,
                question_group__visible_from__lte=timezone.now(),
                question_group__visible_to__gte=timezone.now()
                ).order_by('-pk')

