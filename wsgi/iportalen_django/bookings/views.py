from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse, Http404

from .models import Booking, Bookable, Invoice, BookingSlot, PartialBooking
from .forms import BookingForm

import datetime

from reportlab.pdfgen import canvas
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


def invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="' + invoice_id + '.pdf"'
    p = canvas.Canvas(response)
    p.drawCentredString(300, 750, "VIKTIG FAKTURA!")
    p.drawString(100, 400, "Bokning: " + str(invoice.booking))
    p.drawString(100, 350, "Datum: " + str(invoice.due))

    p.drawString(100, 200, "Att betala: " + str(invoice.total_cost()))

    p.showPage()
    p.save()

    return response


def first_day_of_week(week, year):
    ret = datetime.datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if datetime.date(year, 1, 4).isoweekday() > 4:
        ret -= datetime.timedelta(days=7)
    return ret


def make_booking(request, bookable_id, year=None, week=None):
    if (year is not None) or (week is not None):
        year_range = range(1990, 2300)
        week_range = range(1, 53)

        if (year not in year_range) and (week not in week_range):
            raise Http404("Invalid date, year & week")
        elif week not in week_range:
            raise Http404("Invalid date, week.")
        elif year not in year_range:
            raise Http404("Invalid date, year.")
    else:
        today = datetime.datetime.today().isocalendar()
        year = today[0]
        week = today[1]

    bookable = get_object_or_404(Bookable, pk=bookable_id)
    slots = BookingSlot.objects.filter(bookable__exact=bookable)

    # Find all partial bookings made.
    monday = first_day_of_week(week=week, year=year)
    sunday = monday + datetime.timedelta(days=6)
    booked_slots = PartialBooking.objects.filter(booking__bookable__exact=bookable,
                                                 date__gte=monday,
                                                 date__lte=sunday)

    booking_status_for_week = []
    days_of_week_dict = {0: "måndag",
                         1: "tisdag",
                         2: "onsdag",
                         3: "torsdag",
                         4:  "fredag",
                         5: "lördag",
                         6: "söndag"}

    #  Want to set: Date(Name, day, month), slots, slot status.
    for i in range(0, 7):
        day = {}

        # Add the dates and swedish name.
        day["date"] = monday + datetime.timedelta(days=i)
        day["swe_date"] = days_of_week_dict[day["date"].weekday()]

        #  Loop which checks status for each bookable slot. False meaning it is taken. True it is free.
        day["slots"] = []
        for slot in slots:
            if booked_slots.filter(date__exact=day["date"], slot__exact=slot).exists():
                day["slots"].append((slot, False))
            else:
                day["slots"].append((slot, True))

        booking_status_for_week.append(day)

    if request.method == "POST":
        form = BookingForm(request.POST)
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
    form = BookingForm(instance=booking)

    return render(request, "bookings/book.html", {
        "form": form,
        "bookable_id": bookable_id,
        "booking_status": booking_status_for_week,
    })
