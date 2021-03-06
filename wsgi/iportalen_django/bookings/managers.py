from django.db import models
from .exceptions import InvalidInput, NoSlots, MultipleBookings, MaxLength, TooShortNotice
from django.db import transaction
from .models import PartialBooking, BookingSlot
from django.utils import timezone
from utils.time import combine_date_and_time
from django.utils.translation import ugettext_lazy as _


class BookingManager(models.Manager):
    @transaction.atomic
    def make_a_booking(self, bookable, start_date, end_date, start_slot, end_slot, user):  # TODO: Reduce complexity
        now = timezone.now()
        if start_date < now.date():
            raise InvalidInput(_("Can't book backwards in time."))
        if start_date == now.date() and start_slot.start_time < now.time():
            raise InvalidInput(_("Booking has already started."))
        if combine_date_and_time(start_date, start_slot.start_time) - timezone.timedelta(
                hours=bookable.hours_before_booking) < now:
            raise TooShortNotice(_("Too short notice"))
        if start_date > end_date:
            raise InvalidInput(_("Start date must be before end date."))
        if start_date == end_date and start_slot.start_time > end_slot.start_time:
            raise InvalidInput(_("Start time must be before end time."))
        if self.filter(user=user).exists():
            nr_of_active_bookings = 0
            for b in self.filter(user=user, bookable=bookable):
                active = False
                for p in b.bookings.all():
                    if p.date > now.date():
                        active = True
                    elif p.date == now.date():
                        if p.slot.end_time > now.time():
                            active = True
                if active:
                    nr_of_active_bookings += 1
            if bookable.max_number_of_bookings <= nr_of_active_bookings:
                raise MultipleBookings(_("You have already booked the bookable the maximum number of times in a row"))
        has_next = True
        slot = start_slot
        current_date = start_date
        partial_bookings = []

        slots = BookingSlot.objects.filter(bookable=bookable).order_by("start_time")
        booking = self.model(user=user, bookable=bookable)  # Temporary booking, not saved yet!
        booking.full_clean()
        booking.save()
        if len(slots) == 0:
            raise NoSlots(_("Couldn't find any slots for the given bookable!"))

        while has_next:
            p = PartialBooking(booking=booking,
                               slot=slot,
                               date=current_date)
            p.clean_fields()
            p.clean()
            p.validate_unique()
            partial_bookings.append(p)

            if (current_date == end_date) and (slot == end_slot):
                has_next = False
            else:
                # if last slot of the day, add day and jump to first slot.
                if slot == slots.reverse()[0]:
                    slot = slots[0]
                    current_date = current_date + timezone.timedelta(days=1)
                else:
                    # Go to the next slot.
                    cnt = 0
                    for s in slots:
                        if s == slot:
                            break
                        cnt += 1
                    slot = slots[cnt + 1]
        if len(partial_bookings) > bookable.max_number_of_slots_in_booking:
            raise MaxLength(_("Too many slots in booking"))
        for p in partial_bookings:
            p.save()
        return booking
