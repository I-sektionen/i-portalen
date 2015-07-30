from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotAllowed

from .models import Booking, Bookable
from .forms import MakeBookingForm
"""
- See my bookings
- Make new booking
- Edit booking
- Remove booking
"""


def index(request):
    bookings = Booking.objects.all()
    return render(request, "bookings/index.html", {
        "bookings": bookings,
    })


def my_bookings(request):
    return render(request, "bookings/index.html")


def make_booking(request, id):
    """
    Id - of the bookable item.
    """
    if request.method == 'POST':
        form = MakeBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Check if it already is booked.
            query = Booking.objects.filter(date__exact=booking.date, slot__exact=booking.slot)
            if query.count() > 0:
                return HttpResponseNotAllowed

            # Make sure it is the right user
            if booking.user != request.user:
                return HttpResponseNotAllowed

            # Ensure that the user hasn't booked to much.
            query = Booking.objects.filter(user__exact=booking.user)
            if query.count() > booking.bookable.max_number_of_bookings:
                return HttpResponseNotAllowed

            booking.save()

        else:
            # Send new form bound to the right bookable and user.
            bookable = get_object_or_404(Bookable, id)
            booking = Booking(user=request.user, bookable=bookable)
            form = MakeBookingForm(booking)

            return render(request, "bookings/book.html", {
                "form": form,
            })
