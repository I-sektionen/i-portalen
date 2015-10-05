from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Event
from .exceptions import CouldNotRegisterException
# Create your views here.


def event(request, pk):
    fetched_event = get_object_or_404(Event, pk=pk)
    return render(request, "events/event.html", {
        "event": fetched_event,
    })


@login_required()
def create_event(request):
    return None

@login_required()
def register_to_event(request, pk):
    if request.method == "POST":
        fetched_event = get_object_or_404(Event, pk=pk)
        try:
            fetched_event.register_user(request.user)
        except CouldNotRegisterException as err:
            print("Fel, kunde inte registrera dig på " + err.event.headline + " för att " + err.reason)
    return redirect("event", pk=pk)
