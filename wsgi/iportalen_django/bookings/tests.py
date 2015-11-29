from django.test import TestCase
from user_managements.models import IUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Booking, BookingSlot, Bookable, PartialBooking

# Alla test använder time vilket är native python och inte django time, pallar inte lösa detta
class EventTests(TestCase):
    def setUp(self):
        booker = IUser.objects.create_user(username="testa123")
        random_guy = IUser.objects.create_user(username="testa321")
        creator_pall = IUser.objects.create_user(username="liuid123")
        booker.full_clean()

        bookable = Bookable.objects.create(name="bil", max_number_of_bookings=2, max_number_of_slots_in_booking=10)
        bookable.full_clean()

        b1 = BookingSlot(start_time=timezone.datetime.strptime("08:00", "%H:%M").time(),
                         end_time=timezone.datetime.strptime("12:00", "%H:%M").time(), bookable=bookable)
        b1.full_clean()
        b1.save()

        BookingSlot.objects.create(start_time=timezone.datetime.strptime("12:01", "%H:%M").time(),
                                   end_time=timezone.datetime.strptime("13:00", "%H:%M").time(),
                                   bookable=bookable)
        BookingSlot.objects.create(start_time=timezone.datetime.strptime("13:01", "%H:%M").time(),
                                   end_time=timezone.datetime.strptime("17:00", "%H:%M").time(),
                                   bookable=bookable)

        self.kamera = Bookable.objects.create(name="kamera", max_number_of_bookings=2)

        BookingSlot.objects.create(start_time=timezone.datetime.strptime("12:00", "%H:%M").time(),
                                   end_time=timezone.datetime.strptime("13:00", "%H:%M").time(),
                                   bookable=self.kamera).full_clean()
        BookingSlot.objects.create(start_time=timezone.datetime.strptime("14:00", "%H:%M").time(),
                                   end_time=timezone.datetime.strptime("15:00", "%H:%M").time(),
                                   bookable=self.kamera).full_clean()

    def test_booking_slots(self):
        bookable = Bookable.objects.create(name="kamera2", max_number_of_bookings=2)

        BookingSlot.objects.create(start_time=timezone.datetime.strptime("12:00", "%H:%M").time(),
                                   end_time=timezone.datetime.strptime("13:00", "%H:%M").time(),
                                   bookable=bookable).full_clean()
        BookingSlot.objects.create(start_time=timezone.datetime.strptime("15:00", "%H:%M").time(),
                                   end_time=timezone.datetime.strptime("17:00", "%H:%M").time(),
                                   bookable=bookable).full_clean()
        try:
            s = BookingSlot(start_time=timezone.datetime.strptime("13:00", "%H:%M").time(),
                            end_time=timezone.datetime.strptime("12:00", "%H:%M").time(),
                            bookable=bookable)
            s.full_clean()
            s.save()
        except ValidationError:
            pass

        slots = BookingSlot.objects.filter(bookable=bookable)
        self.assertEqual(len(slots), 2)

    def test_booking_slots_overlap_after(self):
        slots = BookingSlot.objects.filter(bookable=self.kamera)

        check = False
        try:
            b = BookingSlot.objects.create(start_time=timezone.datetime.strptime("12:30", "%H:%M").time(),
                                           end_time=timezone.datetime.strptime("13:30", "%H:%M").time(),
                                           bookable=self.kamera)
            b.full_clean()
        except ValidationError:
            check = True
        self.assertTrue(check)

    def test_booking_slots_overlap_before(self):
        check = False
        try:
            b = BookingSlot.objects.create(start_time=timezone.datetime.strptime("11:30", "%H:%M").time(),
                                           end_time=timezone.datetime.strptime("12:30", "%H:%M").time(),
                                           bookable=self.kamera)
            b.full_clean()
        except ValidationError:
            check = True
        self.assertTrue(check)

    def test_booking_slots_overlap_both(self):
        check = False
        try:
            b = BookingSlot.objects.create(start_time=timezone.datetime.strptime("12:10", "%H:%M").time(),
                                           end_time=timezone.datetime.strptime("12:30", "%H:%M").time(),
                                           bookable=self.kamera)
            b.full_clean()
        except ValidationError:
            check = True
        self.assertTrue(check)

    def test_make_a_booking(self):
        booker = IUser.objects.get(username="testa123")
        bookable = Bookable.objects.get(name="bil")
        slots = BookingSlot.objects.filter(bookable=bookable).order_by("-start_time")

        booking = Booking.objects.make_a_booking(bookable=bookable,
                                                 start_date=timezone.datetime.strptime("2112-10-01", "%Y-%m-%d").date(),
                                                 end_date=timezone.datetime.strptime("2112-10-03", "%Y-%m-%d").date(),
                                                 start_slot=slots[0],
                                                 end_slot=slots[1],
                                                 user=booker)
        self.assertIsNotNone(booking)
        pbookings = PartialBooking.objects.filter(booking=booking)
        self.assertTrue(pbookings.exists())
