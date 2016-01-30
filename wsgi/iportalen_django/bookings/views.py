from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from bookings.exceptions import NoSlots, InvalidInput, MaxLength, MultipleBookings, TooShortNotice
from utils.time import first_day_of_week, daterange, combine_date_and_time
from .models import Booking, Bookable, Invoice, BookingSlot, PartialBooking, FixedCostAmount, VariableCostAmount
from .forms import BookingForm


@login_required()
def index(request):
    bookings = Booking.objects.filter(user=request.user)
    bookables = Bookable.objects.all()
    invoices = Invoice.objects.filter(booking__user=request.user, status=Invoice.SENT)
    return render(request, "bookings/my_bookings.html", {
        "bookings": bookings,
        "bookables": bookables,
        "invoices": invoices,
    })


@login_required()
def invoice(request, invoice_id):
    inv = get_object_or_404(Invoice, pk=invoice_id)
    booking = inv.booking

    #  Must be have permission or be correct user.
    if not (request.user.has_perm("bookings.manage_bookings") or booking.user == request.user):
        return HttpResponseForbidden

    bookable = booking.bookable
    fixed_costs = FixedCostAmount.objects.filter(invoice=inv)
    variable_costs = VariableCostAmount.objects.filter(invoice=inv)
    return render(request, 'bookings/invoice.html', {
        'invoice': inv,
        'booking': booking,
        'bookable': bookable,
        'fixed_costs': fixed_costs,
        'variable_costs': variable_costs,
    })


@login_required()
def make_booking(request, bookable_id, weeks_forward=0):  # TODO: Reduce complexity
    weeks_forward = int(weeks_forward)
    today = timezone.datetime.today() + timezone.timedelta(weeks=weeks_forward)
    today = today.isocalendar()
    year = today[0]
    week = today[1]
    form = BookingForm(request.POST or None)
    bookable = get_object_or_404(Bookable, pk=bookable_id)
    slots = BookingSlot.objects.filter(bookable__exact=bookable)

    # Find all partial bookings made.
    monday = first_day_of_week(week=week, year=year)
    sunday = monday + timezone.timedelta(days=6)
    booked_slots = PartialBooking.objects.filter(booking__bookable__exact=bookable,
                                                 date__gte=monday,
                                                 date__lte=sunday)

    start = []
    end = []
    #  Want to set: Date(Name, day, month), slots, slot status.
    for week_delta in range(0, 16):
        for i in range(0, 7):
            day = {"date": monday + timezone.timedelta(days=i + (week_delta * 7)), "slots": []}

            #  Loop which checks status for each bookable slot. False meaning it is taken. True it is free.
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

    user = request.user
    nr_of_active_bookings = 0
    now = timezone.now()
    for bookings_by_user in Booking.objects.filter(user=user):
        active = False
        for booking_by_user in bookings_by_user.bookings.all():
            if booking_by_user.date > now.date():
                active = True
            elif booking_by_user.date == now.date():
                if booking_by_user.slot.end_time > now.time():
                    active = True
        if active:
            nr_of_active_bookings += 1
    if bookable.max_number_of_bookings <= nr_of_active_bookings:
        messages.warning(
            request,
            "".join(["Du har nu bokat {:} det maximala antalet gånger i rad som du får.",
                     " Avboka eller vänta tills din bokning är över för att göra flera."]).format(bookable.name))

    if request.method == "POST":
        if form.is_valid():
            if bookable.require_phone and not request.user.phone:
                messages.error(request, "Du måste ange ditt telefonnummer för att kunna göra en bokning."
                                        " Klicka på \"konto\" för att ange detta i din profil.")
                return render(request, "bookings/book.html", {
                    "form": form,
                    "bookable_id": bookable_id,
                    "bookable": bookable,
                    "weeks_forward": weeks_forward,
                })
            start_str = form.cleaned_data['start']
            end_str = form.cleaned_data['end']
            start_list = start_str.split("_")
            end_list = end_str.split("_")

            start_date = timezone.datetime.strptime(start_list[0], "%Y%m%d").date()
            end_date = timezone.datetime.strptime(end_list[0], "%Y%m%d").date()
            start_slot = BookingSlot.objects.get(bookable=bookable, start_time=start_list[1])
            end_slot = BookingSlot.objects.get(bookable=bookable, end_time=end_list[1])
            try:
                Booking.objects.make_a_booking(bookable=bookable,
                                               start_date=start_date,
                                               end_date=end_date,
                                               start_slot=start_slot,
                                               end_slot=end_slot,
                                               user=request.user)
                messages.success(request, "Du har bokat {bookable}.".format(bookable=bookable))
                return redirect("bookings:make booking", bookable_id=bookable_id)
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
            except TooShortNotice as e:
                messages.error(request, e.reason)

    return render(request, "bookings/book.html", {
        "form": form,
        "bookable_id": bookable_id,
        "bookable": bookable,
        "weeks_forward": weeks_forward,
    })


@login_required()
def remove_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.user.pk == booking.user.pk:
        booking.delete()
    return redirect("bookings:my bookings")


def api_view(request, bookable_id, weeks_forward=0):
    weeks_forward = int(weeks_forward)
    today = timezone.datetime.today() + timezone.timedelta(weeks=weeks_forward)
    today = today.isocalendar()
    year = today[0]
    week = today[1]
    monday = first_day_of_week(week=week, year=year)

    bookable = get_object_or_404(Bookable, pk=bookable_id)
    slots = BookingSlot.objects.filter(bookable=bookable).order_by("start_time")
    partial_bookings = PartialBooking.objects.filter(booking__bookable=bookable)

    user = request.user
    nr_of_active_bookings = 0
    now = timezone.now()
    for b in Booking.objects.filter(user=user):
        active = False
        for p in b.bookings.all():
            if p.date > now.date():
                active = True
            elif p.date == now.date():
                if p.slot.end_time > now.time():
                    active = True
        if active:
            nr_of_active_bookings += 1

    user_dict = {"nr_of_active_bookings": nr_of_active_bookings}

    bookable_dict = {
        'name': bookable.name,
        'max_number_of_bookings': bookable.max_number_of_bookings,
        'max_number_of_slots_in_booking': bookable.max_number_of_slots_in_booking,
        'hours_before_booking': bookable.hours_before_booking
    }

    # Move to number of weeks forward relative to today, then backup to monday.
    start_date = monday
    end_date = start_date + timezone.timedelta(weeks=2)

    # Från ett datum till sista, skapa en array med datum, slots och huruvida det är bokat eller ej.
    bookings_list = []
    cnt = 0
    for single_date in daterange(start_date, end_date):
        slot_array = []
        cnt += 1
        for slot in slots:
            booked = True
            u = None
            if partial_bookings.filter(date=single_date, slot=slot).exists():
                booked = False
                u = partial_bookings.get(date=single_date, slot=slot).booking.user.username
            blocked = (combine_date_and_time(single_date, slot.start_time) - timezone.timedelta(
                hours=bookable.hours_before_booking)) < timezone.now()

            tmp = {
                'start_time': slot.start_time,
                'end_time': slot.end_time,
                'available': booked,
                'blocked': blocked,
                'user': u,
            }
            slot_array.append(tmp)

        date_info = {
            'weekday': single_date.weekday(),
            'year': single_date.year,
            'month': single_date.month,
            'day': single_date.day,

        }
        bookings_list.append({
            'date': date_info,
            'slots': slot_array,
        })

    data = {
        'user': user_dict,
        'bookable': bookable_dict,
        'bookings': bookings_list,
    }
    return JsonResponse(data)


@permission_required('bookings.manage_bookings')
def create_invoice(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk)
    q = Invoice.objects.filter(booking=booking)
    if not q.exists():
        i = Invoice(status=Invoice.CREATED,
                    booking=booking,
                    )
        i.save()
    else:
        i = q[0]  # take the first one.
    return redirect(reverse("admin:bookings_invoice_change", args=[i.pk]))


@permission_required('bookings.manage_bookings')
def send_invoice_email(request, invoice_pk):
    i = get_object_or_404(Invoice, pk=invoice_pk)
    subject = "Faktura för {name}".format(name=i.booking.bookable, )
    msg = "En ny faktura finns nu tillgänglig åt dig på i-portalen.se." \
          " Du behöver logga in på ditt konto för att ta del av fakturan," \
          " klicka på bokningar upp till höger för att se dina fakturor."
    frm = "bokning@i-portalen.se"  # Todo: Is this reasonable?
    to = i.booking.user.email
    send_mail(subject, msg, frm, [to])
    if i.status == Invoice.CREATED:
        i.status = Invoice.SENT
        i.save()
    messages.success(request, "Ett email har skickats till användaren om fakturan, denna faktura har markerats som skickad.")
    return redirect(reverse("admin:bookings_invoice_change", args=[i.pk]))
