from django.core.exceptions import ValidationError
from django.db import models
from user_managements.models import IUser


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
    start_date = models.DateTimeField(verbose_name="startdatum", help_text="startdatum för perioden")
    end_date = models.DateTimeField(verbose_name="slutdatum", help_text="slutdatum för perioden")
    name = models.CharField(verbose_name="namn", help_text="Ex, 2016 VT1", max_length=255)
    courses = models.ManyToManyField(Course, verbose_name="kurser", help_text="kurser att utvärdera")

    class Meta:
        verbose_name = 'läsperiod'
        verbose_name_plural = 'läsperioder'

    def __str__(self):
        return "{name}".format(name=self.name)

    def save(self, *args, **kwargs):
        if self.start_time > self.end_time:
            raise ValidationError('End time must be set after start time.')

        periods = Period.objects.all()
        if self.id:
            periods.exclude(pk=self.id)
        for period in periods:
            if self.start_time < period.start_time:  # Före
                if self.end_time > period.start_time:
                    raise ValidationError('The periods are end- and start times are invalid. They are overlapping. before')
            else:  # Efter
                if self.start_time < period.end_time:
                    raise ValidationError("The periods are end- and start times are invalid. They are overlapping. after")
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