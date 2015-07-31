from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models import Q


class Bookable(models.Model):
    name = models.CharField(max_length=512)
    max_number_of_bookings = models.IntegerField()

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
    bookable = models.ForeignKey(Bookable)

    slot = models.ForeignKey(
        BookingSlot,
        on_delete=models.CASCADE,
        limit_choices_to=Q( bookable__exact = bookable)
        )

    date = models.DateField()

    class Meta:
        permissions = (("unlimited_num_of_bookings", "Unlimited number of bookings"),)
        unique_together = (("slot", "bookable", "date"),)

    def __str__(self):
        return self.bookable.name + ": " + str(self.date) + ", " + str(self.slot) + " av " + self.user.username


class FixedCostTemplate(models.Model):
    title = models.CharField(max_length=400)
    add_tax = models.BooleanField(default=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class FixedCostAmount(models.Model):
    template = models.ForeignKey(FixedCostTemplate)

    @property
    def total(self):
        total = self.units * self.price
        if self.add_tax or self.template.tax is None:
            return total * self.tax
        else:
            return total

    def __str__(self):
        return self.title


class VariableCostTemplate(models.Model):
    title = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    add_tax = models.BooleanField(default=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title


class VariableCostAmount(models.Model):
    units = models.DecimalField(max_digits=9, decimal_places=2)
    template = models.ForeignKey(VariableCostTemplate)
    invoice = models.ForeignKey(AbstractBaseInvoice)

    @property
    def total(self):
        t = self.template
        total = self.units * t.price
        if t.add_tax:
            return total * t.tax
        else:
            return total

    def __str__(self):
        return self.template.title


class AbstractBaseInvoice(models.Model):
    INVOICE_STATUSES = (
        ('cr', 'Created'),
        ('se', 'Sent'),
        ('an', 'Terminated'),
        ('pa', 'Payed')
    )
    due = models.DateField(default=datetime.now()+timedelta(days=30))
    booking = models.ForeignKey(Booking)

    fixed_costs = models.ManyToManyField(FixedCostAmount, related_name="%(app_label)s_%(class)s_related")

    variable_costs = models.ManyToManyField(VariableCostAmount, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True


class CustomInvoice(AbstractBaseInvoice):
    recipient = models.CharField(max_length=400)
    email = models.CharField(max_length=800)


class UserInvoice(AbstractBaseInvoice):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL)