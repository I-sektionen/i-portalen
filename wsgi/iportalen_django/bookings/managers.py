from django.db import models
from django.core.exceptions import ValidationError
"""
from .models import PartialBooking, BookingSlot

from datetime import timedelta


class BookingManager(models.Manager):

    def make_a_booking(self, bookable, start_date, end_date, start_slot, end_slot, user):
        has_next = False
        slot = start_slot
        date = start_date
        partial_bookings = []

        slots = BookingSlot.filter(bookable=bookable).order_by("-start_time")
        booking = self.model(user=user, bookable=bookable)  # Temporary booking, not saved yet!
        if len(slots) == 0:
            return False

        while has_next:
            try:
                p = PartialBooking(booking=booking,
                                   slot=slot,
                                   date=date)
                p.full_clean(validate_unique=True)
                partial_bookings.append(p)
            except ValidationError:
                return False

            # Try to book next slot.

            if (date >= end_date) and (slot == end_slot):
                has_next = False
            else:
                # if last slot of the day, add day and jump to first slot.
                if slots == slots.reverse[0]:
                    slot = slots[0]
                    date = date + timedelta(days=1)
                else:
                    # Go to the next slot.
                    cnt = 0
                    for s in slots:
                        if s == slot:
                            break
                        cnt = + 1
                    if cnt + 1 >= len(slots):
                        slot = slots[0]
                    else:
                        slot = slots[cnt+1]
        booking.save()
        return booking
"""