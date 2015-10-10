from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from .forms import EventForm
from .models import Event
from .exceptions import CouldNotRegisterException
# Create your views here.


def view_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    can_administer = event.can_administer(request.user)
    return render(request, "events/event.html", {
        "event": event,
        "can_administer": can_administer,
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
def administer_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/administer_event.html', {
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


def check_in(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        print("Add me!")
