from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse, Http404, JsonResponse
from django.utils import timezone

from bookings.exceptions import NoSlots, InvalidInput, MaxLength, MultipleBookings
from .models import Booking, Bookable, Invoice, BookingSlot, PartialBooking
from .forms import BookingForm
from utils.time import first_day_of_week
import datetime

#from reportlab.pdfgen import canvas
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
    return redirect('index')
"""
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
"""

def make_booking(request, bookable_id, year=None, week=None):
    if (year is not None) or (week is not None):
        year_range = range(1990, 2300)
        week_range = range(1, 53)
        year = int(year)
        week = int(week)
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
        print(week)
    form = BookingForm(request.POST or None)
    bookable = get_object_or_404(Bookable, pk=bookable_id)
    slots = BookingSlot.objects.filter(bookable__exact=bookable)

    # Find all partial bookings made.
    monday = first_day_of_week(week=week, year=year)
    sunday = monday + datetime.timedelta(days=6)
    booked_slots = PartialBooking.objects.filter(booking__bookable__exact=bookable,
                                                 date__gte=monday,
                                                 date__lte=sunday)

    start = []
    end = []
    #  Want to set: Date(Name, day, month), slots, slot status.
    for week_delta in range(0, 4):
        for i in range(0, 7):
            day = {}

            # Add the dates and swedish name.
            day["date"] = monday + datetime.timedelta(days=i + (week_delta * 7))

            #  Loop which checks status for each bookable slot. False meaning it is taken. True it is free.
            day["slots"] = []
            for slot in slots:
                if booked_slots.filter(date__exact=day["date"], slot__exact=slot).exists():
                    day["slots"].append((slot, False))
                else:
                    day["slots"].append((slot, True))
                    start.append(("{date}_{time}".format(date=day['date'].strftime("%Y%m%d"), time=slot.start_time),
                                  "{date} {time}".format(date=day['date'].strftime("%Y-%m-%d"), time=slot.start_time)))
                    end.append(("{date}_{time}".format(date=day['date'].strftime("%Y%m%d"), time=slot.end_time),
                                "{date} {time}".format(date=day['date'].strftime("%Y-%m-%d"), time=slot.end_time)))

        form.fields['start'].choices = start
        form.fields['end'].choices = end
        if request.method == "POST":
            if form.is_valid():
                start = form.cleaned_data['start']
                end = form.cleaned_data['end']
                start_list = start.split("_")
                end_list = end.split("_")
                start_date = datetime.datetime.strptime(start_list[0], "%Y%m%d").date()
                end_date = datetime.datetime.strptime(end_list[0], "%Y%m%d").date()
                start_slot = BookingSlot.objects.get(bookable=bookable, start_time=start_list[1])
                end_slot = BookingSlot.objects.get(bookable=bookable, end_time=end_list[1])
                try:
                    Booking.objects.make_a_booking(bookable=bookable,
                                                   start_date=start_date,
                                                   end_date=end_date,
                                                   start_slot=start_slot,
                                                   end_slot=end_slot,
                                                   user=request.user)
                    messages.success(request, "YAY")
                    return redirect("make_booking", bookable_id=bookable_id)
                except NoSlots as e:
                    messages.error(request, e.reason)
                except InvalidInput as e:
                    messages.error(request, e.reason)
                except ValidationError:
                    messages.error(request, "There exist already booked slots within your booking.")
                except MaxLength as e:
                    messages.error(request, e.reason)
                except MultipleBookings as e:
                    messages.error(request, e.reason)

    return render(request, "bookings/book.html", {
        "form": form,
        "bookable_id": bookable_id,
    })


def api_view(request, bookable_id, weeks_forward=0):
    bookable = get_object_or_404(Bookable, pk=bookable_id)
    slots = BookingSlot.objects.filter(bookable=bookable).order_by("start_time")
    partial_bookings = PartialBooking.objects.filter(booking__bookable=bookable)

    bookable_dict = {
        'name': bookable.name,
        'max_number_of_bookings': bookable.max_number_of_bookings,
        'max_number_of_slots_in_booking': bookable.max_number_of_slots_in_booking
    }

    # Move to number of weeks forward relative to today, then backup to monday.
    start_date = timezone.now()
    start_date += datetime.timedelta(weeks=weeks_forward, days=1)  # Extra day is if today is monday.
    while start_date.weekday() != 0:
        start_date -= datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=14)

    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + datetime.timedelta(n)

    # Från ett datum till sista, skapa en array med datum, slots och huruvida det är bokat eller ej.
    bookings_dict = []
    cnt = 0
    for single_date in daterange(start_date, end_date):
        slot_array = []
        cnt += 1
        for slot in slots:
            booked = True
            if partial_bookings.filter(date=single_date, slot=slot).exists():
                booked = False
            tmp = {
                'start_time': slot.start_time,
                'end_time': slot.end_time,
                'available': booked,
            }
            slot_array.append(tmp)

        date_info = {
            'weekday': single_date.weekday(),
            'year': single_date.year,
            'month': single_date.month,
            'day': single_date.day,

        }
        bookings_dict.append({
            'date': date_info,
            'slots': slot_array,
        })

    data = {
        'bookable': bookable_dict,
        'bookings': bookings_dict,
    }
    return JsonResponse(data)

