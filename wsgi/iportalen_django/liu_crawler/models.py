from django.db import models


class Result(models.Model):
    name = models.CharField(max_length=255)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
