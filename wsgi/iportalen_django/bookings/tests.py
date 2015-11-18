from django.test import TestCase
from user_managements.models import IUser

#from .models import Booking, BookingSlot, Bookable

# Create your tests here.
"""
class EventTests(TestCase):
    def setUp(self):
        booker = IUser.objects.create_user(username="testa123")
        random_guy = IUser.objects.create_user(username="testa321")
        creator_pall = IUser.objects.create_user(username="liuid123")

        bookable = Bookable.objects.create(name="bil", max_number_of_bookings=2)
        BookingSlot.objects.create(start_time="08:00", end_time="12:00", bookable=bookable)
        BookingSlot.objects.create(start_time="12:01", end_time="13:00", bookable=bookable)
        BookingSlot.objects.create(start_time="13:01", end_time="16:00", bookable=bookable)

    def test_make_a_booking(self):

        self.assertFalse(True)
"""