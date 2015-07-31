from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

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
    bookables = Bookable.objects.all()
    return render(request, "bookings/index.html", {
        "bookings": bookings,
        "bookables": bookables,
    })

"""
def my_bookings(request):
    return render(request, "bookings/index.html")
"""


def make_booking(request, bookable_id):
    """
    Id - of the bookable item.
    """
    bookable = get_object_or_404(Bookable, pk=bookable_id)
    if request.method == "POST":
        form = MakeBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.bookable = bookable

            # Make sure it is the right user
            booking.user = request.user

            # Ensure that the user hasn't booked to much.
            query = Booking.objects.filter(user__exact=booking.user)
            if query.count() > booking.bookable.max_number_of_bookings:
                return HttpResponseForbidden()

            booking.save()
            return redirect("make_booking", bookable_id=bookable_id)

    # Send new form bound to the right bookable and user.
    booking = Booking(user=request.user, bookable=bookable)
    form = MakeBookingForm(instance=booking)

    return render(request, "bookings/book.html", {
        "form": form,
        "bookable_id": bookable_id,
    })
