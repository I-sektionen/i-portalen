__author__ = 'Magnus Forzelius & Jesper Lehtonen'
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from utils.validators import liu_id_validator
from tags.models import Tag
import os

class Continent(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Världsdel")
        verbose_name_plural = _("Världsdelar")

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50)
    in_continent = models.ForeignKey(Continent, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Land")
        verbose_name_plural = _("Länder")

    def __str__(self):
        return self.name

    def get_country_list(self):
        return self.objects.all()

class City(models.Model):
    name = models.CharField(max_length=50)
    in_country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Stad")
        verbose_name_plural = _("Städer")

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=50)
    in_city = models.ForeignKey(City, on_delete=models.CASCADE)
    freemover = models.BooleanField(default=False)
    exchange_with_liu = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Skola")
        verbose_name_plural = _("Skolor")

    def __str__(self):
        return self.name

class Liu_Course(models.Model):
    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=20)
    is_compulsary = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Liukurs")
        verbose_name_plural = _("Liukurser")

    def __str__(self):
        return self.name

class Exchange_Course(models.Model):

    TECH_PROFILES = (
        ('Datateknik', "Datateknik"),
        ('Energiteknik', "Energiteknik"),
        ('Maskinteknik', "Maskinteknik"),
        ('Bioteknik', "Bioteknik"),
        ('Systemteknik', "Systemteknik"),
        ('Ingen', "Ingen")
    )

    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=20)
    year = models.IntegerField()
    technical_profile = models.CharField(verbose_name='Teknisk inriktning', max_length=12, choices=TECH_PROFILES, default='NONE')
    in_school = models.ForeignKey(School, on_delete=models.CASCADE)
    corresponding_liu_course = models.ForeignKey(Liu_Course, on_delete=models.CASCADE)

    # Add attribute "credits", and att the credits/hp quota in school model
    # A course can be required in several tech profile

    class Meta:
        verbose_name = _("Utlandskurs")
        verbose_name_plural = _("Utlandskurser")

    def __str__(self):
        return self.name


def _file_path(instance, filename):
    return os.path.join(
        'travel_stories', str(instance.about_school.pk), filename
    )

class Travel_Story(models.Model):
    #Change from file to form
    about_school = models.ForeignKey(School, on_delete=models.CASCADE)
    added_by_user = models.CharField(verbose_name=_("liu-id"), max_length=10)
    headline = models.CharField(
      verbose_name=_("rubrik"),
      max_length=255,
      help_text=_("Rubriken till reseberättelsen"))
    lead = models.TextField(
        verbose_name=_("ingress"),
        help_text=_("Ingressen är den text som syns i reseberättelse."))
    prep_text = models.TextField(
        verbose_name=_("förberedelser"),
        help_text=_("Var det några särskilda förberedelser som krävdes?  Har du några generella tips gällande ansökan? Visum?"),
        null=True,
        blank=True)
    location_text = models.TextField(
        verbose_name=_("landet och staden"),
        help_text=_("Hur upplevdes landet? Staden? Kultur? Billigt eller dyrt?"),
        null=True,
        blank=True)
    school_text = models.TextField(
        verbose_name=_("skolan"),
        help_text=_("Geografisk placering i staden?  Hur var campus?  Var det lätt att träffa lokalbefolkning?  Hur var studentlivet? Kurser: var det lätt/svårt att få kurser? Var de lätta/svåra att få tillgodoräknade?"),
        null=True,
        blank=True)
    studies_text = models.TextField(
        verbose_name=_("studier"),
        help_text=_("Hur var nivån på kurserna?  Råd angående att välja kurser på plats?  Svårt att hitta kurser på engelska?  Hur var språket? (framförallt för de som läser ii eller som inte läste på engelska)"),
        null=True,
        blank=True)
    living_text = models.TextField(
        verbose_name=_("boende"),
        help_text=_("Hur bodde du?  Hur hittade du ditt boende? Tips på eventuell mäklare eller liknande? Vilka alternativ finns?  Priser och standard? "),
        null=True,
        blank=True)
    sparetime_text = models.TextField(
        verbose_name=_("fritid"),
        help_text=_("Vad gör man på fritiden?  Resor?  Tips på saker man inte får missa"),
        null=True,
        blank=True)
    other_text = models.TextField(
        verbose_name=_("övrigt"),
        help_text=_("Brödtext syns när en reseberättelse visas enskilt."),
        null=True,
        blank=True)
    #tags = models.ManyToManyField(
     #   Tag,
     #   verbose_name=_("tag"),
      #  blank=True,
       # help_text=_("Håll ner Ctrl för att markera flera."))

    class Meta:
         verbose_name = _("Reseberättelse")
         verbose_name_plural = _("Reseberättelser")

    def __str__(self):
        return self.headline

    #def get_absolute_url(self):
     #   """Get url of object"""
      #  return reverse(self)
    #self.about_school
