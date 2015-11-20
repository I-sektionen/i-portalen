from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import PartialBooking, BookingSlot

from datetime import timedelta


class BookingManager(models.Manager):
    @transaction.atomic
    def make_a_booking(self, bookable, start_date, end_date, start_slot, end_slot, user):
        has_next = True
        slot = start_slot
        current_date = start_date
        partial_bookings = []

        slots = BookingSlot.objects.filter(bookable=bookable).order_by("start_time")
        booking = self.model(user=user, bookable=bookable)  # Temporary booking, not saved yet!
        booking.full_clean()
        booking.save()
        if len(slots) == 0:
            # Throw error
            return None

        count = 0
        while has_next:
            try:
                p = PartialBooking(booking=booking,
                                   slot=slot,
                                   date=current_date)
                p.clean_fields()
                p.clean()
                p.validate_unique()
                #p.full_clean(validate_unique=True)
                partial_bookings.append(p)
            except ValidationError:
                # Do not catch.
                return None

            # Try to book next slot.

            count += 1
            if count == 10:
                print("Något gick nog galet =/")
                has_next = False



            if (current_date == end_date) and (slot == end_slot):
                has_next = False
            else:
                # if last slot of the day, add day and jump to first slot.
                if slot == slots.reverse()[0]:
                    slot = slots[0]
                    current_date = current_date + timedelta(days=1)
                else:
                    # Go to the next slot.
                    cnt = 0
                    for s in slots:
                        if s == slot:
                            break
                        cnt = + 1
                    slot = slots[cnt+1]
        booking.save()
        for p in partial_bookings:
            p.save()
        return booking
