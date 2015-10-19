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
from .models import Event
from .exceptions import CouldNotRegisterException
from user_managements.models import IUser
# Create your views here.


def view_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    can_administer = event.can_administer(request.user)

    return render(request, "events/event.html", {
        "event": event,
        "can_administer": can_administer,
        "registered": event.registered(request.user),
    })


@login_required()
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.approved = False
            event.save()
            messages.success(request, "Ditt evenemang än nu skapat, det väntar nu på att godkännas av infU.")
            return redirect("front page")
        else:
            return render(request, 'events/create_event.html', {
                'form': form,
            })

    form = EventForm
    return render(request, 'events/create_event.html', {
        'form': form,
    })


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
        return HttpResponseForbidden  # Nope.


@login_required()
def preregistrations_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/event_preregistrations.html', {
            'event': event,
        })
    else:
        return HttpResponseForbidden  # Nope.

@login_required()
def participants_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/event_participants.html', {
            'event': event,
        })
    else:
        return HttpResponseForbidden  # Nope.


@login_required()
def check_in(request, pk):
    event = get_object_or_404(Event, pk=pk)
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
                'form': form, 'event.pk': event.pk
            })
            if event_user in event.preregistrations or form.cleaned_data["force_check_in"] == True:
                try:
                    event.check_in(IUser.objects.get(username=liu_id))
                    messages.success(request, "Det lyckades")
                    return render(request, 'events/event_check_in.html', {
                        'form': form, 'event.pk': event.pk
                     })
                except:
                    messages.error(request, "Redan anmäld som deltagere")
            else:
                if event_user in event.reserves:
                    messages.error(request, "Användare är anmäld som reserv")
                else:
                    messages.error(request, "Användare inte anmäld på eventet")
                reserve = True
                return render(request, 'events/event_check_in.html', {'form': form, 'event.pk': event.pk, 'reserve': reserve})

        else:
            return render(request, 'events/event_check_in.html', {
                'form': form, 'event.pk': event.pk
            })

    form = CheckForm
    return render(request, 'events/event_check_in.html', {
        'form': form, 'event.pk': event.pk
    })

@login_required()
def all_unapproved_events(request):
    if request.user.has_perm("event.can_approve_event"):
        events = Event.objects.filter(approved=False, end__gte=timezone.now())
        return render(request, 'events/approve_event.html', {'events': events})
    else:
        raise PermissionDenied


@login_required()
@transaction.atomic
def approve_event(request, event_id):
    if request.user.has_perm("event.can_approve_event"):
        a = Event.objects.get(pk=event_id)
        a.approved = True
        a.save()
        return redirect(all_unapproved_events)
    else:
        raise PermissionDenied


@login_required()
def unapprove_event(request, event_id):
    if request.user.has_perm("event.can_approve_event"):
        a = Event.objects.get(pk=event_id)
        # a.draft = True
        a.save()
        message = ("Eventet har gått tillbaka till utkast läget, maila gärna <a href='mailto:" +
                   a.user.email +
                   "?Subject=Avslag%20publicering%20av%20event' target='_top'>" +
                   a.user.email +
                   "</a> med en förklaring till avslaget.<br>" +
                   "<a href='/event/unapproved'>Tillbaka till listan över artiklar att godkänna.</a>")
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
