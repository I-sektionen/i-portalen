from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.urlresolvers import reverse
from .managers import IUserManager
from django.utils import timezone
from organisations.models import Organisation
from utils.validators import liu_id_validator, validate_year
from django.utils.translation import ugettext_lazy as _

YEAR_CHOICES = []
for r in range(1969, (timezone.now().year+10)):
    YEAR_CHOICES.append((r, r))


class BachelorProfile(models.Model):
    name = models.CharField(verbose_name=_("namn"), max_length=255)
    info = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = _("kandidatprofil")
        verbose_name_plural = _("kandidatprofiler")

    def __str__(self):
        return self.name


class MasterProfile(models.Model):
    name = models.CharField(verbose_name=_("namn"), max_length=255)
    info = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = _("masterprofil")
        verbose_name_plural = _("masterprofiler")

    def __str__(self):
        return self.name


# Liuid as username and <liuid>@student.liu.se as email
class IUser(AbstractBaseUser, PermissionsMixin):
    MAN = 'm'
    WOMEN = 'w'
    OTHER = 'o'  # Other / non-binary
    UNSPECIFIED = 'u'  # Don't want to specify
    GENDER_OPTIONS = (
        (MAN, _("Man")),
        (WOMEN, _("Kvinna")),
        (OTHER, _("Annat / icke-binär")),
        (UNSPECIFIED, _("Vill ej ange"))
    )

    YEAR1 = '1'
    YEAR2 = '2'
    YEAR3 = '3'
    YEAR4 = '4'
    YEAR5 = '5'
    PAUSE = 'p'
    STUDY_YEARS = (
        (YEAR1, _("åk 1")),
        (YEAR2, _("åk 2")),
        (YEAR3, _("åk 3")),
        (YEAR4, _("åk 4")),
        (YEAR5, _("åk 5")),
        (PAUSE, _("uppehåll"))
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
        (UNSPECIFIED_CLASS, _("ej angivet")),
        (A_CLASS, _("a-klassen")),
        (B_CLASS, _("b-klassen")),
        (C_CLASS, _("c-klassen")),
        (D_CLASS, _("d-klassen")),
        (E_CLASS, _("e-klassen")),
        (F_CLASS, _("f-klassen")),
        (IA_CLASS, _("ia-klassen")),
        (IB_CLASS, _("ib-klassen")),
    )

    # basic fields
    username = models.CharField(verbose_name=_("LiU-ID"), unique=True, max_length=8, validators=[liu_id_validator])
    email = models.EmailField(verbose_name=_("Email"))
    first_name = models.CharField(verbose_name=_("förnamn"), max_length=50, null=True, blank=True)
    last_name = models.CharField(verbose_name=_("efternamn"), max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("gick med datum"))
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    # our fields
    p_nr = models.CharField(verbose_name=_("personnummer"), max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name=_("adress"), max_length=255, null=True, blank=True)
    zip_code = models.CharField(verbose_name=_("postnummer"), max_length=255, null=True, blank=True)
    city = models.CharField(verbose_name=_("ort"), max_length=255, null=True, blank=True)
    gender = models.CharField(verbose_name=_("kön"),
                              max_length=1, null=True, blank=True, choices=GENDER_OPTIONS, default=None)
    allergies = models.TextField(verbose_name=_("allergier"), null=True, blank=True)
    start_year = models.IntegerField(
        verbose_name=_("startår"), choices=YEAR_CHOICES, default=timezone.now().year, validators=[validate_year])
    current_year = models.CharField(verbose_name=_("nuvarande årskurs"),
                                    max_length=1,
                                    choices=STUDY_YEARS,
                                    default=YEAR1,
                                    blank=False,
                                    null=True)
    klass = models.CharField(verbose_name=_("klass"),
                             max_length=1,
                             choices=CLASSES,
                             default=UNSPECIFIED_CLASS,
                             blank=False,
                             null=True)
    bachelor_profile = models.ForeignKey(BachelorProfile, null=True, blank=True, verbose_name=_("kandidatprofil"),
                                         on_delete=models.SET_NULL,
                                         help_text=_("Välj Ej valt om du inte har valt kandidatprofil."))
    master_profile = models.ForeignKey(MasterProfile, null=True, blank=True, verbose_name=_("masterprofil"),
                                       on_delete=models.SET_NULL,
                                       help_text=_("Välj Ej valt om du inte har valt kandidatprofil."))
    rfid_number = models.CharField(verbose_name=_("rfid"), max_length=255, null=True, blank=True)
    is_member = models.NullBooleanField(verbose_name=_("Är medlem?"), blank=True, null=True, default=None)

    must_edit = models.BooleanField(verbose_name=_("Måste uppdatera info"), default=True)

    phone = models.CharField(verbose_name=_("Telefon"), max_length=255, null=True, blank=True)

    #modified = models.DateTimeField(editable=False)

    objects = IUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        try:
            return self.first_name.capitalize() + " " + self.last_name.capitalize()
        except:
            return self.username

    def get_absolute_url(self):
        """Get url of object"""
        return reverse('user_management:profile page', kwargs={'liu_id': self.username})

    def get_short_name(self):
        return self.username

    def _get_email(self):
        return self.username + "@student.liu.se"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """Override save to set created and modifed date before saving."""
        self.modified = timezone.now()
        super(IUser, self).save(*args, **kwargs)

    @property
    def update_from_kobra_url(self):
        return reverse("user_management:update user from kobra", kwargs={'liu_id': self.username})

    class Meta:
        verbose_name = _("användare")
        verbose_name_plural = _("användare")
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
    date_subscribed = models.DateTimeField(auto_now_add=True, verbose_name=_("prenumererar sedan datum"))

    class Meta:
        verbose_name = _("ipikureprenumerant")
        verbose_name_plural = _("ipikureprenumeranter")
        permissions = (('can_view_subscribers', 'Can view subscribers'),)

    def __str__(self):
        return "{user}: {year}-{month}-{day}".format(
            user=self.user.username,
            year=self.date_subscribed.year,
            month=self.date_subscribed.month,
            day=self.date_subscribed.day)
