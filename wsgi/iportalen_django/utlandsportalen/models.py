from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Land")
        verbose_name_plural = _("Länder")

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=50)
    in_country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Skola")
        verbose_name_plural = _("Skolor")

    def __str__(self):
        return self.name

class Liu_Course(models.Model):
    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=20)
    is_compulsary = models.BooleanField()

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

    class Meta:
        verbose_name = _("Utlandskurs")
        verbose_name_plural = _("Utlandskurser")

    def __str__(self):
        return self.name