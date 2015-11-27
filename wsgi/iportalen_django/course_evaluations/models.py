from django.db import models
from user_managements.models import IUser


class Course(models.Model):
    code = models.CharField(verbose_name='kurskod', max_length=10, unique=True)
    name = models.CharField(verbose_name='kursnamn', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'kurs'
        verbose_name_plural = 'kurser'


class Reward(models.Model):
    name = models.CharField(verbose_name='belöning', max_length=255)

    class Meta:
        verbose_name = 'belöning'
        verbose_name_plural = 'belöningar'


class Period(models.Model):
    start_date = models.DateTimeField(verbose_name="startdatum", help_text="startdatum för perioden")
    end_date = models.DateTimeField(verbose_name="slutdatum", help_text="slutdatum för perioden")
    name = models.CharField(verbose_name="namn", help_text="Ex, VT1 2016", max_length=255)
    courses = models.ManyToManyField(Course, verbose_name="kurser", help_text="kurser att utvärdera")

    class Meta:
        verbose_name = 'läsperiod'
        verbose_name_plural = 'läsperioder'


class Evaluation(models.Model):
    course = models.ForeignKey(Course, verbose_name="kurs", on_delete=models.SET_NULL, null=True, blank=False)
    reward = models.ForeignKey(Reward, verbose_name="belönig", on_delete=models.SET_NULL, null=True, blank=False)
    period = models.ForeignKey(Period, verbose_name="läsperiod", on_delete=models.SET_NULL, null=True, blank=False)
    user = models.ForeignKey(IUser, verbose_name="kurs", null=False, blank=False)

    class Meta:
        unique_together = (('course', 'period'),)  # Make sure only one booking on one data and timeslot.
        verbose_name = 'kursutvärderare'
        verbose_name_plural = 'kursutvärderare'