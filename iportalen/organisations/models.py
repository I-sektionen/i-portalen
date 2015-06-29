from iportalen import settings
from django.db import models

# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField()
    contact_info = models.TextField()
    image = models.FileField(upload_to='organisations')
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="leader")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="members")