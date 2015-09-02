import datetime
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import IUserManager


YEAR_CHOICES = []
for r in range((datetime.datetime.now().year-10), (datetime.datetime.now().year+10)):
    YEAR_CHOICES.append((r,r))


class BachelorProfile(models.Model):
    name = models.CharField(verbose_name='namn', max_length=255)
    info = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "kandidatprofil"
        verbose_name_plural = "kandidatprofiler"

    def __str__(self):
        return self.name


class MasterProfile(models.Model):
    name = models.CharField(verbose_name='namn', max_length=255)
    info = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "masterprofil"
        verbose_name_plural = "masterprofiler"

    def __str__(self):
        return self.name


# Liuid as username and <liuid>@student.liu.se as email
class IUser(AbstractBaseUser, PermissionsMixin):
    liu_id_validator = RegexValidator(r'^[a-zA-Z]{5}\d{3}$')

    # basic fields
    username = models.CharField(verbose_name='LiU-ID', unique=True, max_length=8, validators=[liu_id_validator])
    first_name = models.CharField(verbose_name='förnamn', max_length=50, null=True, blank=True)
    last_name = models.CharField(verbose_name='efternamn', max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='gick med datum')
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    # our fields
    p_nr = models.CharField(verbose_name='personnummer', max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name='adress', max_length=255, null=True, blank=True)
    zip_code = models.CharField(verbose_name='postnummer', max_length=255, null=True, blank=True)
    city = models.CharField(verbose_name='ort', max_length=255, null=True, blank=True)
    gender = models.CharField(verbose_name='kön', max_length=255, null=True, blank=True)
    allergies = models.TextField(verbose_name='allergier', null=True, blank=True)
    start_year = models.IntegerField(verbose_name='start år', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    expected_exam_year = models.IntegerField(verbose_name='förväntat examens år', choices=YEAR_CHOICES, default=datetime.datetime.now().year+5)
    bachelor_profile = models.ForeignKey(BachelorProfile, null=True, blank=True, verbose_name='kandidatprofil')
    master_profile = models.ForeignKey(MasterProfile, null=True, blank=True, verbose_name='masterprofil', )
    rfid_number = models.CharField(verbose_name='rfid', max_length=255, null=True, blank=True)

    objects = IUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        #fullname = self.first_name+" "+self.last_name
        return self.username

    def get_short_name(self):
        return self.username

    def _get_email(self):
        return self.username + "@student.liu.se"

    email = property(_get_email)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "användare"
        verbose_name_plural = "användare"
