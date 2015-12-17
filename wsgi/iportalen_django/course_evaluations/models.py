from itertools import chain

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from user_managements.models import IUser
from django.utils import timezone
from .managers import PeriodManager, YearManager

PERIOD_CHOICES = [('VT1', 'VT1'), ('VT2', 'VT2'), ('HT1', 'HT1'), ('HT2', 'HT2')]


class Year(models.Model):
    YEAR_CHOICES = []
    for r in range(2014, (timezone.now().year+50)):
        YEAR_CHOICES.append((r,r))
    year = models.IntegerField(verbose_name="år", unique=True, choices=YEAR_CHOICES,
                               default=timezone.now().year)
    vt1 = models.ForeignKey("Period", verbose_name="VT1", related_name="vt1", )
    vt2 = models.ForeignKey("Period", verbose_name="VT2", related_name="vt2")
    ht1 = models.ForeignKey("Period", verbose_name="HT1", related_name="ht1")
    ht2 = models.ForeignKey("Period", verbose_name="HT2", related_name="ht2")
    objects = YearManager
    class Meta:
        verbose_name = 'år'
        verbose_name_plural = 'år'

    def __str__(self):
        return "{year}".format(year=self.year)

    def get_absolute_url(self):
        return reverse('course_evaluations:admin year', kwargs={'year': self.year})


class Course(models.Model):
    code = models.CharField(verbose_name='kurskod', max_length=10, unique=True)
    name = models.CharField(verbose_name='kursnamn', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'kurs'
        verbose_name_plural = 'kurser'

    def __str__(self):
        return "{code} - {name}".format(code=self.code, name=self.name)


class Reward(models.Model):
    name = models.CharField(verbose_name='namn', max_length=255, unique=True)
    active = models.BooleanField(verbose_name='aktiv', default=True)
    class Meta:
        verbose_name = 'belöning'
        verbose_name_plural = 'belöningar'

    def __str__(self):
        return "{name}".format(name=self.name)


class Period(models.Model):
    start_date = models.DateField(verbose_name="startdatum", help_text="startdatum för perioden")
    end_date = models.DateField(verbose_name="slutdatum", help_text="slutdatum för perioden")
    name = models.CharField(verbose_name="namn", help_text="Ex, VT1", choices=PERIOD_CHOICES, max_length=255)
    courses = models.ManyToManyField(Course, verbose_name="kurser", help_text="kurser att utvärdera")
    objects = PeriodManager
    class Meta:
        verbose_name = 'läsperiod'
        verbose_name_plural = 'läsperioder'

    def __str__(self):
        return "{name} {start} - {end}".format(name=self.name, start=self.start_date, end=self.end_date)

    def get_absolute_url(self):
        return reverse('course_evaluations:admin period', kwargs={'pk': self.pk})

    @property
    def get_year(self):
        year = None
        if self.ht1.all():
            year = self.ht1.all()
        elif self.ht2.all():
            year = self.ht2.all()
        elif self.vt1.all():
            year = self.vt1.all()
        elif self.vt2.all():
            year = self.vt2.all()
        return year[0]

    def clean(self):
        super(Period, self).clean()
        if self.start_date > self.end_date:
            raise ValidationError('End time must be set after start time.')

        periods = Period.objects.all()
        if self.pk:
            periods = periods.exclude(pk=self.pk)
        for period in periods:
            if self.start_date < period.start_date:  # Före
                if self.end_date > period.end_date:
                    raise ValidationError('The periods are end- and start times are invalid. They are overlapping. before')
            else:  # Efter
                if self.start_date < period.end_date:
                    raise ValidationError("The periods are end- and start times are invalid. They are overlapping. after")

    def save(self, *args, **kwargs):

        super(Period, self).save(*args, **kwargs)

    def get_free_courses(self):
        ev_set = self.evaluation_set.all()
        # Om en kurs går över 2 perioder ska den bara gå att anmäla sig till i en av dem.
        if self.name == "HT2":
            ev_set = list(chain(ev_set, self.ht2.all()[0].ht1.evaluation_set.all()))
        if self.name == "VT2":
            ev_set = list(chain(ev_set, self.vt2.all()[0].vt1.evaluation_set.all()))

        taken = set()
        for t in ev_set:
            taken.add(t.course)
        return set(self.courses.all()).difference(taken)

    def update_courses_from_list(self, course_list):
        original = self.courses.values_list('pk')
        for a in course_list:
            if (int(a),) in original:
                pass
            else:
                self.courses.add(Course.objects.get(pk=a))
        for a in original:
            if str(a[0]) in course_list:
                pass
            else:
                self.courses.remove(Course.objects.get(pk=str(a[0])))


class Evaluation(models.Model):
    course = models.ForeignKey(Course, verbose_name="kurs", on_delete=models.SET_NULL, null=True, blank=False)
    reward = models.ForeignKey(Reward, verbose_name="belönig", on_delete=models.SET_NULL, null=True, blank=False)
    period = models.ForeignKey(Period, verbose_name="läsperiod", on_delete=models.SET_NULL, null=True, blank=False)
    user = models.ForeignKey(IUser, verbose_name="användare", null=False, blank=False)
    evaluated = models.BooleanField(verbose_name="genomförd", default=False)

    class Meta:
        unique_together = (('course', 'period'),)  # Make sure only one booking on one data and timeslot.
        verbose_name = 'kursutvärderare'
        verbose_name_plural = 'kursutvärderare'

    def __str__(self):
        return "{course}, {period}, {user}".format(
            course=self.course.code, period=str(self.period), user=str(self.user))