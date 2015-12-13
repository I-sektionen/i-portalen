from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from user_managements.models import IUser
from django.utils import timezone


class Year(models.Model):
    YEAR_CHOICES = []
    for r in range(2014, (timezone.now().year+50)):
        YEAR_CHOICES.append((r,r))
    year = models.IntegerField(verbose_name="år", unique=True, choices=YEAR_CHOICES,
                               default=timezone.now().year)
    vt1 = models.ForeignKey("Period", verbose_name="VT1", related_name="vt1")
    vt2 = models.ForeignKey("Period", verbose_name="VT2", related_name="vt2")
    ht1 = models.ForeignKey("Period", verbose_name="HT1", related_name="ht1")
    ht2 = models.ForeignKey("Period", verbose_name="HT2", related_name="ht2")

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
    name = models.CharField(verbose_name='belöning', max_length=255)

    class Meta:
        verbose_name = 'belöning'
        verbose_name_plural = 'belöningar'

    def __str__(self):
        return "{name}".format(name=self.name)


class Period(models.Model):
    start_date = models.DateField(verbose_name="startdatum", help_text="startdatum för perioden")
    end_date = models.DateField(verbose_name="slutdatum", help_text="slutdatum för perioden")
    name = models.CharField(verbose_name="namn", help_text="Ex, 2016 VT1", max_length=255)
    courses = models.ManyToManyField(Course, verbose_name="kurser", help_text="kurser att utvärdera")

    class Meta:
        verbose_name = 'läsperiod'
        verbose_name_plural = 'läsperioder'

    def __str__(self):
        return "{name} {start} - {end}".format(name=self.name, start=self.start_date, end=self.end_date)

    def get_absolute_url(self):
        return reverse('course_evaluations:admin period', kwargs={'pk': self.pk})

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
        taken = set()
        for t in ev_set:
            taken.add(t.course)
        return set(self.courses.all()).difference(taken)


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