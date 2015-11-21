from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


class Bookable(models.Model):
    name = models.CharField(max_length=512)
    max_number_of_bookings = models.IntegerField(default=1)  # Maximum number of simultaneous bookings.
    max_number_of_slots_in_booking = models.IntegerField(default=1)  # Max length of booking

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('make_booking', args=[str(self.pk)])

    class Meta:
        verbose_name = 'bokningsbart objekt'
        verbose_name_plural = 'bokningsbara objekt'


class BookingSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    bookable = models.ForeignKey("Bookable")

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('End time must be set after start time.')

        # Create: Should just check if it fulfills all criterias.
        # Update: Should check same things, but find out which element being updated.

        slots = BookingSlot.objects.filter(bookable=self.bookable)
        for slot in slots:
            if slot == self:  # This does not work....
                break  # In case of update might self and slot be the same.

            if self.start_time < slot.start_time:  # Före
                if self.end_time > slot.start_time:
                    raise ValidationError('The timeslots are end- and start times are invalid. They are overlapping. Före')
            else:  # Efter
                if self.start_time < slot.end_time:
                    raise ValidationError("The timeslots are end- and start times are invalid. They are overlapping. Efter")
        super(BookingSlot, self).clean()

    def __str__(self):
        return str(self.start_time) + " - " + str(self.end_time) + " (" + self.bookable.name + ")"

    class Meta:
        verbose_name = 'bokningsblock'
        verbose_name_plural = 'bokningsblock'


class PartialBooking(models.Model):
    booking = models.ForeignKey("Booking", related_name='bookings')
    slot = models.ForeignKey("BookingSlot")
    date = models.DateField()

    class Meta:
        unique_together = (('slot', 'date'),)  # Make sure only one booking on one data and timeslot.
        verbose_name = 'delbokning'
        verbose_name_plural = 'delbokninar'


class Invoice(models.Model):
    NOT_CREATED = 'NC'
    CREATED = 'CR'
    SENT = 'SE'
    TERMINATED = 'TR'
    PAYED = 'PA'
    INVOICE_STATUSES = (
        (CREATED, 'Skapad'),
        (SENT, 'Skickad'),
        (TERMINATED, 'Avbruten'),
        (PAYED, 'Betald')
    )
    status = models.CharField(max_length=2,
                              choices=INVOICE_STATUSES,
                              default=CREATED)

    due = models.DateField(default=datetime.now()+timedelta(days=30), verbose_name='förfallo dag')
    booking = models.ForeignKey("Booking", verbose_name='bokning')

    def get_absolute_url(self):
        return reverse('bookings.views.invoice_pdf', args=[str(self.pk)])

    class Meta:
        verbose_name = 'faktura'
        verbose_name_plural = 'fakturor'

    def __str__(self):
        return 'Faktura för ' + str(self.booking)

    def total_cost(self):
        fixed = FixedCostAmount.objects.filter(invoice__exact=self)
        variable = VariableCostAmount.objects.filter(invoice__exact=self)
        total = 0
        for f in fixed:
            total += f.total
        for v in variable:
            total += v.total
        return total


class FixedCostTemplate(models.Model):
    title = models.CharField(max_length=400, verbose_name='namn')
    add_tax = models.BooleanField(default=True, verbose_name='Lägg till moms?')
    tax = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='moms')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='belopp')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'mall'
        verbose_name_plural = 'mallar för fasta kostnader'


class FixedCostAmount(models.Model):
    template = models.ForeignKey(FixedCostTemplate)
    quantity = models.PositiveIntegerField(default=1)

    invoice = models.ForeignKey(Invoice)

    @property
    def total(self):
        t = self.template
        total = self.quantity * t.amount
        if t.add_tax and (t.tax is not None):
            return total * t.tax
        else:
            return total

    def __str__(self):
        return self.template.title


class VariableCostTemplate(models.Model):
    title = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    add_tax = models.BooleanField(default=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    unit_name = models.CharField(max_length=30, default="st")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'mall'
        verbose_name_plural = 'mallar för rörliga kostnader'

class VariableCostAmount(models.Model):
    units = models.DecimalField(max_digits=9, decimal_places=2)
    template = models.ForeignKey(VariableCostTemplate)
    invoice = models.ForeignKey(Invoice)

    @property
    def total(self):
        t = self.template
        total = self.units * t.price
        if t.add_tax and (t.tax is not None):
            return total * t.tax
        else:
            return total

    def __str__(self):
        return self.template.title

# This has to be here. Sorry! (PartialBooking is not loaded when this import occurs otherwise.)
# TODO: Refactor this model file inte several parts.
from .managers import BookingManager


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="bokad av")
    bookable = models.ForeignKey(Bookable, verbose_name='boknings objekt')

    objects = BookingManager()

    class Meta:
        permissions = (("unlimited_num_of_bookings", "Unlimited number of bookings"),)
        verbose_name = 'bokning'
        verbose_name_plural = 'bokningar'

    def __str__(self):
        return self.bookable.name + ", av " + self.user.username