from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _
__author__ = 'jonathan'


class IUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError(_('User must have a username'))

        user = self.model(username=username)
        user.email = username+"@student.liu.se"
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
