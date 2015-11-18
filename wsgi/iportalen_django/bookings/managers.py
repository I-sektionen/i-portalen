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

        while has_next:
            try:
                print(booking)
                print(slot)
                print(current_date)
                p = PartialBooking(booking=booking,
                                   slot=slot,
                                   date=current_date)
                print("0")
                p.clean_fields()
                print("1!")
                p.clean()
                print("2!")
                p.validate_unique()
                print("3!")
                #p.full_clean(validate_unique=True)
                partial_bookings.append(p)
            except ValidationError:
                # Do not catch.
                return None

            # Try to book next slot.

            if (current_date >= end_date) and (slot == end_slot):
                has_next = False
            else:
                # if last slot of the day, add day and jump to first slot.
                if slots == slots.reverse()[0]:
                    slot = slots[0]
                    current_date = current_date + timedelta(days=1)
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
