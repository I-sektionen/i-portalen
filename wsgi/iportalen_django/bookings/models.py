from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from utils.time import has_passed, combine_date_and_time, now_plus_one_month


class Bookable(models.Model):
    name = models.CharField(max_length=512)
    max_number_of_bookings = models.IntegerField(default=1)  # Maximum number of simultaneous bookings.
    max_number_of_slots_in_booking = models.IntegerField(default=1)  # Max length of booking
    hours_before_booking = models.IntegerField(default=24)  # must book at least this many hours befor booking starts.
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bookings:make booking', args=[str(self.pk)])

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
                    raise ValidationError(
                        'The timeslots are end- and start times are invalid. They are overlapping. Före')
            else:  # Efter
                if self.start_time < slot.end_time:
                    raise ValidationError(
                        "The timeslots are end- and start times are invalid. They are overlapping. Efter")
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
    NOT_CREATED = 'NC'  # Used by the Booking model to indicated that this instance does not exist.
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

    due = models.DateField(default=now_plus_one_month, verbose_name='förfallo dag')
    booking = models.ForeignKey("Booking", verbose_name='bokning')
    ocr = models.CharField(max_length=11, verbose_name="OCR nummer", null=True, blank=True)

    def _calculate_ocr(self):
        def digits_of(n):
            return [int(d) for d in str(n)]

        def check_sum(s):
            digits = digits_of(num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]

            checksum = 0
            checksum += sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10

        # Number based on primary key
        num = str(self.pk)
        num = "1337" + num
        while len(num) < 9:
            num += "0"
        print(len(num))
        num += "10"  # Should be 10 long now, eleven wih check number.
        check_num = check_sum(num)
        if check_num != 0:
            num = num[:-1]
            num += str(10-check_num)
        self.ocr = num
        self.save()

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)
        if self.ocr is None or len(self.ocr) == 0:
            self._calculate_ocr()

    class Meta:
        verbose_name = 'faktura'
        verbose_name_plural = 'fakturor'

    def __str__(self):
        return 'Faktura'

    def get_absolute_url(self):
        return reverse('bookings:invoice view', kwargs={'invoice_id': self.pk})

    def _total_cost(self):
        fixed = FixedCostAmount.objects.filter(invoice__exact=self)
        variable = VariableCostAmount.objects.filter(invoice__exact=self)
        total = 0
        for f in fixed:
            total += f.amount
        for v in variable:
            total += v.amount
        return total
    total = property(_total_cost)


class FixedCostTemplate(models.Model):
    title = models.CharField(max_length=400, verbose_name='namn')
    tax = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='momssats')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='belopp ink moms')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'mall'
        verbose_name_plural = 'mallar för fasta kostnader'


class FixedCostAmount(models.Model):
    template = models.ForeignKey(FixedCostTemplate)
    quantity = models.PositiveIntegerField(default=1)

    invoice = models.ForeignKey(Invoice)

    def _calculate_total(self):
        return self.quantity * self.template.amount

    def _calculate_tax(self):
        tot = self._calculate_total()
        tax = self.template.tax
        return round(tot - (tot / (1 + tax)), 2)

    tax_amount = property(_calculate_tax)
    amount = property(_calculate_total)

    def __str__(self):
        return self.template.title


class VariableCostTemplate(models.Model):
    title = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=9, decimal_places=2)
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

    def _calculate_total(self):
        return round(self.units * self.template.price, 2)

    def _calculate_tax(self):
        tot = self._calculate_total()
        tax = self.template.tax
        return round(tot - (tot / (1 + tax)), 2)

    def _unit_type(self):
        return self.template.unit_name

    def _unit_price(self):
        return self.template.price

    tax_amount = property(_calculate_tax)
    amount = property(_calculate_total)
    unit_name = property(_unit_type)
    unit_price = property(_unit_price)

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
        permissions = (("unlimited_num_of_bookings", "Unlimited number of bookings"),
                       ("manage_bookings", "Manage bookings"))
        verbose_name = 'bokning'
        verbose_name_plural = 'bokningar'

    def __str__(self):
        td = self.get_time_of_booking()
        return self.bookable.name + " bokad från: " + str(td["start"].strftime("%H:%M %d-%b")) + " till: " + \
            str(td["end"].strftime("%H:%M %d-%b"))

    def _can_be_unbooked(self):
        time = self.get_time_of_booking()
        if has_passed(time["start"] - timezone.timedelta(hours=self.bookable.hours_before_booking)):
            return False
        return True

    can_be_unbooked = property(_can_be_unbooked)

    def get_time_of_booking(self):
        start_time = None
        end_time = None
        start_date = None
        end_date = None
        for p in self.bookings.all():
            if not start_time:
                start_time = p.slot.start_time
            if not end_time:
                end_time = p.slot.end_time
            if not start_date:
                start_date = p.date
            if not end_date:
                end_date = p.date
            if start_time > p.slot.start_time:
                start_time = p.slot.start_time
            if end_time < p.slot.end_time:
                end_time = p.slot.end_time
            if start_date > p.date:
                start_date = p.date
            if end_date < p.date:
                end_date = p.date

        return {"start": combine_date_and_time(start_date, start_time),
                "end": combine_date_and_time(end_date, end_time)}

    def _start_time(self):
        return self.get_time_of_booking()['start']

    start_time = property(_start_time)
