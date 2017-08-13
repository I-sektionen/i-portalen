from django.utils import timezone

__author__ = 'jers'
from django.core.management.base import BaseCommand
from user_managements.models import IUser

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        users = IUser.objects.all()
        for user in users:
            if user.modified < timezone.now()-timezone.timedelta(days=30):
                user.must_edit = True
                user.save()