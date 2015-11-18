from django.test import TestCase
from user_managements.models import IUser
from datetime import date, time

from .models import Booking, BookingSlot, Bookable, PartialBooking


class EventTests(TestCase):
    def setUp(self):
        booker = IUser.objects.create_user(username="testa123")
        random_guy = IUser.objects.create_user(username="testa321")
        creator_pall = IUser.objects.create_user(username="liuid123")
        booker.full_clean()

        bookable = Bookable.objects.create(name="bil", max_number_of_bookings=2)
        bookable.full_clean()

        b1 = BookingSlot(start_time=time(hour=8, minute=0), end_time=time(hour=12, minute=0), bookable=bookable)
        b1.full_clean()
        b1.save()

        BookingSlot.objects.create(start_time=time(hour=12, minute=1), end_time=time(hour=13, minute=0), bookable=bookable)
        BookingSlot.objects.create(start_time=time(hour=13, minute=1), end_time=time(hour=17, minute=0), bookable=bookable)

    def test_make_a_booking(self):
        booker = IUser.objects.get(username="testa123")
        bookable = Bookable.objects.get(name="bil")
        slots = BookingSlot.objects.filter(bookable=bookable).order_by("-start_time")

        print(slots[0])
        print(slots[1])
        print("ssdfdfs")


        booking = Booking.objects.make_a_booking(bookable=bookable,
                                                 start_date=date(year=2012, month=10, day=1),
                                                 end_date=date(year=2012, month=10, day=2),
                                                 start_slot=slots[0],
                                                 end_slot=slots[1],
                                                 user=booker)
        self.assertIsNotNone(booking)
        pbookings = PartialBooking.objects.filter(booking=booking)
        print(pbookings)
        self.assertTrue(pbookings.exists())
