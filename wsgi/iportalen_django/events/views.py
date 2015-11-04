from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import csv


from .forms import EventForm, CheckForm
from .models import Event, EntryAsPreRegistered, EntryAsReserve
from .exceptions import CouldNotRegisterException
from user_managements.models import IUser
# Create your views here.


def view_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    can_administer = event.can_administer(request.user)
    if event.status == Event.APPROVED or can_administer:
        return render(request, "events/event.html", {
            "event": event,
            "can_administer": can_administer,
            "registered": event.registered(request.user),
        })
    else:
        return HttpResponseForbidden()


@login_required()
def register_to_event(request, pk):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        try:
            event.register_user(request.user)
            messages.success(request, "Du är nu registrerad på eventet.")
        except CouldNotRegisterException as err:
            messages.error(request, "Fel, kunde inte registrera dig på " + err.event.headline + " för att " + err.reason + ".")
    return redirect("event", pk=pk)


@login_required()
def register_as_reserve(request, pk):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        entry = event.register_reserve(request.user)
        messages.success(request, "Du är nu anmäld som reserv på eventet, du har plats nr. " + str(entry.position()) + ".")
    return redirect("event", pk=pk)


@login_required()
def administer_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/administer_event.html', {
            'event': event,
        })
    else:
        return HttpResponseForbidden()  # Nope.


@login_required()
def preregistrations_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/event_preregistrations.html', {
            'event': event,
        })
    else:
        return HttpResponseForbidden()  # Nope.

@login_required()
def participants_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/event_participants.html', {
            'event': event,
        })
    else:
        return HttpResponseForbidden()  # Nope.

@login_required()
def reserves_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event_reserves = event.reserves_object()
    if event.can_administer(request.user):
        return render(request, 'events/event_reserves.html', {
            'event': event,
            'event_reserves': event_reserves,
        })
    else:
        return HttpResponseForbidden()  # Nope.


@login_required()
def check_in(request, pk):
    event = get_object_or_404(Event, pk=pk)
    can_administer = event.can_administer(request.user)
    reserve = False
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            liu_id = form.cleaned_data["liu"]
            event_user = None
            try:
                event_user = IUser.objects.get(username=liu_id)
            except ObjectDoesNotExist:
                messages.error(request, "Användaren finns inte i databasen")
                form = CheckForm()
                return render(request, 'events/event_check_in.html', {
                'form': form, 'event': event, "can_administer": can_administer,
            })
            if event_user in event.preregistrations or form.cleaned_data["force_check_in"] == True:
                try:
                    event.check_in(IUser.objects.get(username=liu_id))
                    messages.success(request, "Det lyckades")
                    return render(request, 'events/event_check_in.html', {
                        'form': form, 'event': event, "can_administer": can_administer,
                     })
                except:
                    messages.error(request, "Redan anmäld som deltagere")
            else:
                if event_user in event.reserves:
                    messages.error(request, "Användare är anmäld som reserv")
                else:
                    messages.error(request, "Användare inte anmäld på eventet")
                reserve = True
                return render(request, 'events/event_check_in.html', {'form': form, 'event': event, 'reserve': reserve, "can_administer": can_administer,})

        else:
            return render(request, 'events/event_check_in.html', {
                'form': form, 'event': event, "can_administer": can_administer,
            })

    form = CheckForm
    return render(request, 'events/event_check_in.html', {
        'form': form, 'event': event, "can_administer": can_administer,
    })

@login_required()
def all_unapproved_events(request):
    if request.user.has_perm("event.can_approve_event"):
        events = Event.objects.filter(status=Event.BEING_REVIEWED, end__gte=timezone.now())
        return render(request, 'events/approve_event.html', {'events': events})
    else:
        raise PermissionDenied


@login_required()
@transaction.atomic
def approve_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.approve(request.user):
        return redirect(all_unapproved_events)
    else:
        raise PermissionDenied


@login_required()
def unapprove_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.reject(request.user):
        # TODO: Ganska horribel lösning...
        message = ("Eventet har gått avslagits, maila gärna <a href='mailto:" +
                   event.user.email +
                   "?Subject=Avslag%20publicering%20av%20event' target='_top'>" +
                   event.user.email +
                   "</a> med en förklaring till avslaget.<br>" +
                   "<a href='/event/unapproved'>Tillbaka till listan över event att godkänna.</a>")
        return render(request, 'articles/confirmation.html', {'message': message})
    else:
        raise PermissionDenied


@login_required()
def CSV_view_participants(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participants.txt"'

    writer = csv.writer(response)
    writer.writerow(['These are your participants:'])

    event = get_object_or_404(Event, pk=pk)
    participants = event.participants

    for user in participants:
        writer.writerow([user.username, user.first_name, user.last_name, user.email])

    return response

@login_required()
def CSV_view_preregistrations(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="preregistrations.txt"'

    writer = csv.writer(response)
    writer.writerow(['These are your preregistrations:'])

    event = get_object_or_404(Event, pk=pk)
    preregistrations = event.preregistrations

    for user in preregistrations:
        writer.writerow([user.username, user.first_name, user.last_name, user.email])

    return response


@login_required()
def unregister(request, pk):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        try:
            event.deregister_user(request.user)
            messages.success(request, "Du är nu avregistrerad på eventet.")
        except CouldNotRegisterException as err:
            messages.error(request, "Fel, kunde inte avregistrera dig på " + err.event.headline + " för att " + err.reason + ".")
    return redirect("event", pk=pk)


def event_calender(request):
    return render(request, "events/calender.html")


@login_required()
def registered_on_events(request):
    entry_as_preregistered = EntryAsPreRegistered.objects.filter(user=request.user)
    entry_as_reserve = EntryAsReserve.objects.filter(user=request.user)
    reserve_events = []
    preregistrations_events = []
    for e in entry_as_preregistered:
        if e.event.end >= timezone.now():
            preregistrations_events.append(e)
    for e in entry_as_reserve:
        if e.event.end >= timezone.now():
            reserve_events.append(e)
    return render(request, "events/registerd_on_events.html",
                  {"reserve_events": reserve_events, "preregistrations_events": preregistrations_events})


@login_required()
def events_by_user(request):
    user_events = Event.objects.filter(user=request.user, end__gte=timezone.now()).order_by('-visible_from')
    return render(request, 'events/my_events.html', {
        'user_events': user_events
    })


@login_required()
def create_or_modify_event(request, pk=None):
    if pk:  # if pk is set we modify an existing event.
        event = get_object_or_404(Event, pk=pk)
        if not event.can_administer(request.user):
            return HttpResponseForbidden()
        form = EventForm(request.POST or None, instance=event)
    else:  # new event.
        form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)

            if form.cleaned_data['draft'] == True:
                draft = True
            else:
                draft = False

            status = event.get_new_status(draft)
            event.status = status["status"]
            event.user = request.user

            if status["new"]:
                event.replacing_id = event.id
                event.id = None

            event.save()
            form.save_m2m()
            event.refresh_from_db()
            pk = event.id
            messages.success(request, "Dina ändringar har sparats.")
            return redirect('event', pk=pk)
        else:
            messages.error(request, "Det uppstod ett fel, se detaljer nedan.")
            return render(request, 'events/create_event.html', {
                'form': form,
            })
    return render(request, 'events/create_event.html', {
        'form': form,
    })
