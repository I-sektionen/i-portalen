from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.urlresolvers import reverse
from .managers import IUserManager
from django.utils import timezone
from organisations.models import Organisation
from utils.validators import liu_id_validator

YEAR_CHOICES = []
for r in range(1969, (timezone.now().year+10)):
    YEAR_CHOICES.append((r, r))


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
    MAN = 'm'
    WOMEN = 'w'
    OTHER = 'o'  # Other / non-binary
    UNSPECIFIED = 'u'  # Don't want to specify
    GENDER_OPTIONS = (
        (MAN, 'Man'),
        (WOMEN, 'Kvinna'),
        (OTHER, 'Annat / icke-binär'),
        (UNSPECIFIED, 'Vill ej ange')
    )

    YEAR1 = '1'
    YEAR2 = '2'
    YEAR3 = '3'
    YEAR4 = '4'
    YEAR5 = '5'
    PAUSE = 'p'
    STUDY_YEARS = (
        (YEAR1, 'åk 1'),
        (YEAR2, 'åk 2'),
        (YEAR3, 'åk 3'),
        (YEAR4, 'åk 4'),
        (YEAR5, 'åk 5'),
        (PAUSE, 'uppehåll')
    )

    A_CLASS = 'a'
    B_CLASS = 'b'
    C_CLASS = 'c'
    D_CLASS = 'd'
    E_CLASS = 'e'
    F_CLASS = 'f'
    IA_CLASS = 'x'
    IB_CLASS = 'y'
    UNSPECIFIED_CLASS = 'u'
    CLASSES = (
        (UNSPECIFIED_CLASS, 'ej angivet'),
        (A_CLASS, 'a-klassen'),
        (B_CLASS, 'b-klassen'),
        (C_CLASS, 'c-klassen'),
        (D_CLASS, 'd-klassen'),
        (E_CLASS, 'e-klassen'),
        (F_CLASS, 'f-klassen'),
        (IA_CLASS, 'ia-klassen'),
        (IB_CLASS, 'ib-klassen'),
    )

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
    gender = models.CharField(verbose_name='kön',
                              max_length=1, null=True, blank=True, choices=GENDER_OPTIONS, default=None)
    allergies = models.TextField(verbose_name='allergier', null=True, blank=True)
    start_year = models.IntegerField(verbose_name='startår', choices=YEAR_CHOICES, default=timezone.now().year)
    current_year = models.CharField(verbose_name='nuvarande årskurs',
                                    max_length=1,
                                    choices=STUDY_YEARS,
                                    default=YEAR1,
                                    blank=False,
                                    null=True)
    klass = models.CharField(verbose_name="klass",
                             max_length=1,
                             choices=CLASSES,
                             default=UNSPECIFIED_CLASS,
                             blank=False,
                             null=True)
    bachelor_profile = models.ForeignKey(BachelorProfile, null=True, blank=True, verbose_name='kandidatprofil',
                                         on_delete=models.SET_NULL)
    master_profile = models.ForeignKey(MasterProfile, null=True, blank=True, verbose_name='masterprofil',
                                       on_delete=models.SET_NULL)
    rfid_number = models.CharField(verbose_name='rfid', max_length=255, null=True, blank=True)
    is_member = models.NullBooleanField(verbose_name="Är medlem?", blank=True, null=True, default=None)

    objects = IUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        try:
            return self.first_name.capitalize() + " " + self.last_name.capitalize()
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
        permissions = (('can_view_users', 'Can view users'),)

    def get_organisations(self):
        organisations = []
        groups = self.groups.all()
        if groups:
            for g in groups:
                organisations = organisations + list(Organisation.objects.filter(group=g))
        return organisations
    organisations = property(get_organisations)


class IpikureSubscriber(models.Model):
    user = models.OneToOneField(IUser, null=True, blank=True)
    date_subscribed = models.DateTimeField(auto_now_add=True, verbose_name='prenumererar sedan datum')

    class Meta:
        verbose_name = "ipikureprenumerant"
        verbose_name_plural = "ipikureprenumeranter"
        permissions = (('can_view_subscribers', 'Can view subscribers'),)

    def __str__(self):
        return "{user}: {year}-{month}-{day}".format(user=self.user.username, year=self.date_subscribed.year, month=self.date_subscribed.month, day=self.date_subscribed.day)
