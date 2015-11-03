import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.urlresolvers import reverse
from .managers import IUserManager
from django.utils import timezone
from organisations.models import Organisation
from utils.validators import liu_id_validator

YEAR_CHOICES = []
for r in range(1969, (datetime.datetime.now().year+10)):
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

    # basic fields
    username = models.CharField(verbose_name='LiU-ID', unique=True, max_length=8, validators=[liu_id_validator])
    email = models.EmailField(verbose_name='Email')
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
    start_year = models.IntegerField(verbose_name='startår', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    expected_exam_year = models.IntegerField(verbose_name='förväntat examensår', choices=YEAR_CHOICES, default=datetime.datetime.now().year+5)
    bachelor_profile = models.ForeignKey(BachelorProfile, null=True, blank=True, verbose_name='kandidatprofil')
    master_profile = models.ForeignKey(MasterProfile, null=True, blank=True, verbose_name='masterprofil', )
    rfid_number = models.CharField(verbose_name='rfid', max_length=255, null=True, blank=True)
    is_member = models.NullBooleanField(verbose_name="Är medlem?", blank=True, null=True, default=None)

    objects = IUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # This is where the menu options for a specific user is determined.
    @property
    def get_menu_choices(self):

        menu_choices = []  # List of extra menu choices.

        menu_choices.append(('Lägg upp innehåll', reverse('create content')))  # Everyone can create article.

        menu_choices.append(('Min sida', reverse('mypage_view') ))

        # Need some python magic here, so the other three rows are not necessary,
        # can't figure it out, also a bit tired right now

        if self.article_set.filter(visible_to__gte=timezone.now()):
             menu_choices.append(('Mina Artiklar', reverse('articles by user')))

        menu_choices.append(('Mina Anmälningar', reverse('registered_on_events')))

        if self.has_perm("articles.can_approve_article"):
            menu_choices.append(('Godkänn Innehåll', reverse('approve content')))  # With perm to edit articles.

        if self.is_staff:
            menu_choices.append(('Admin', '/admin'))  # Staff users who can access Admin page.

        if self.has_perm("user_managements.add_iuser"):
            menu_choices.append(("Lägg till Liu-idn i whitelist", reverse('add users to whitelist')))

        return menu_choices

    def get_full_name(self):
        try:
            return self.first_name+" "+self.last_name
        except:
            return self.username

    def get_short_name(self):
        return self.username

    def _get_email(self):
        return self.username + "@student.liu.se"

    # email = property(_get_email)

    def __str__(self):
        return self.username

    @property
    def update_from_kobra_url(self):
        return reverse("update user from kobra", kwargs={'liu_id': self.username})

    class Meta:
        verbose_name = "användare"
        verbose_name_plural = "användare"

    def get_organisations(self):
        organisations = []
        groups = self.groups.all()
        if groups:
            for g in groups:
                organisations = organisations + list(Organisation.objects.filter(group=g))
        return organisations
