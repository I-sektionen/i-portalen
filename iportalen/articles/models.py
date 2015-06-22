from django.db import models
import datetime


class Tag(models.Model):
    name_sv = models.TextField()
    name_en = models.TextField()

    def __str__(self):
        return self.name_sv


class Article(models.Model):
    headline_sv = models.CharField(max_length=255)
    lead_sv = models.TextField()
    body_sv = models.TextField()

    headline_en = models.CharField(max_length=255)
    lead_en = models.TextField()
    body_en = models.TextField()

    visible_from = models.DateTimeField()
    visible_to = models.DateTimeField()
    approved = models.BooleanField()
    # access  # TODO: access restrictions

    author = models.TextField()  # TODO: change to reference to author
    tags = models.ManyToManyField(Tag)

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        self.updated = datetime.datetime.today()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.headline_sv
