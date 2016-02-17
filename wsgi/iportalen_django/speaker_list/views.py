from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from events.models import Event
from .exceptions import SpeakerListException
from .utils import (
    add_to_speakerlist,
    next_speaker,
    remove_from_speakerlist
)
from .models import SpeakerList
from .forms import SpeakerForm


@login_required()
def speaker_list(request, pk):  # TODO: Reduce complexity
    if request.method == 'POST':
        try:
            event = Event.objects.get(pk=pk)
            if not event.can_administer(request.user):
                raise PermissionDenied
        except:
            return JsonResponse({"status": _("Inget event med detta idnummer.")})
        form = SpeakerForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['method'] == "add":
                return add_to_speakerlist(event, form.cleaned_data['speech_nr'])
            elif form.cleaned_data['method'] == "pop":
                return next_speaker(event)
            elif form.cleaned_data['method'] == "remove":
                return remove_from_speakerlist(event, form.cleaned_data['speech_nr'])
            elif form.cleaned_data['method'] == "clear":
                SpeakerList.objects.clear(event=event)
                return JsonResponse({'status': 'ok'})
            elif form.cleaned_data['method'] == "shuffle":
                SpeakerList.objects.shuffle(event=event)
                return JsonResponse({'status': 'ok'})
            elif form.cleaned_data['method'] == "all":
                return JsonResponse({"status": "ok", "speaker_list": SpeakerList.objects.show_queue(event=event)})
            else:
                return JsonResponse({"status": _("Ange ett korrekt kommando.")})
    else:
        return JsonResponse({})


@login_required()
def speaker_list_user_add_self(request, pk):
    event = get_object_or_404(Event, pk=pk)
    try:
        SpeakerList.objects.add(event=event, user=request.user)
        messages.success(request, _("Du har skrivit upp dig på talarlistan!"))
    except SpeakerListException as e:
        messages.error(request, str(e.reason))
    return redirect(reverse('events:user view', kwargs={'pk': event.pk}))


@login_required()
def speaker_list_user_remove_self(request, pk):
    event = get_object_or_404(Event, pk=pk)
    try:
        SpeakerList.objects.remove(event=event, user=request.user)
        messages.success(request, _("Du har strukit dig från talarlistan!"))
    except SpeakerListException as e:
        messages.error(request, str(e.reason))
    return redirect(reverse('events:user view', kwargs={'pk': event.pk}))


@login_required()
def speaker_list_display(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'speaker_list/display_speaker_list.html', {
        'speaker_list': SpeakerList.objects.show_queue(event=event), 'event': event
    })


@login_required()
def administer_speaker_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'speaker_list/administer_speaker_list.html', {
        'event': event
    })
