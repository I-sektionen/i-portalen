from django.db import models
from django.conf import settings


class Bookable(models.Model):
    name = models.CharField(max_length=512)
    max_number_of_bookings = models.IntegerField(max_length=100)
    def __str__(self):
        return self.name


class BookingSlot(models.Model):
    number = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    bookable = models.ForeignKey(Bookable)

    def __str__(self):
        return str(self.start_time) + " - " + str(self.end_time) + " (" + self.bookable.name + ")"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Bokad av")
    slot = models.ForeignKey(BookingSlot)
    bookable = models.ForeignKey(Bookable)
    date = models.DateField()

    def __str__(self):
        return self.bookable.name + ": " + str(self.date) + ", " + str(self.slot) + " av " + self.user.username






