from django.db import models


class LetsEncrypt(models.Model):
    url = models.CharField(max_length=255)
    text = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
