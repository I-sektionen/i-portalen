from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
from events.models import EntryAsParticipant, Event
from .forms import SpeakerForm


@login_required()
def speaker_list(request, pk):  # TODO: Reduce complexity
    if request.method == 'POST':
        try:
            event = Event.objects.get(pk=pk)
            if not event.can_administer(request.user):
                return HttpResponseForbidden()
        except:
            return JsonResponse({"status": _("Inget event med detta idnummer.")})
        form = SpeakerForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['method'] == "add":
                speech_nr = form.cleaned_data['speech_nr']
                try:
                    event.add_speaker_to_queue(speech_nr)
                    return JsonResponse({'status': 'ok'})
                except:
                    return JsonResponse({"status": _("Ingen användare med det talarnummret.")})
            elif form.cleaned_data['method'] == "pop":
                event.remove_first_speaker_from_queue()
                return JsonResponse({'status': 'ok'})
            elif form.cleaned_data['method'] == "remove":
                speech_nr = form.cleaned_data['speech_nr']
                try:
                    event.remove_speaker_from_queue(speech_nr)
                    return JsonResponse({'status': 'ok'})
                except:
                    return JsonResponse({"status": _("Ingen användare med det talarnummret.")})
            elif form.cleaned_data['method'] == "clear":
                event.clear_speaker_queue()
                return JsonResponse({'status': 'ok'})
            elif form.cleaned_data['method'] == "all":
                return JsonResponse({"status": "ok", "speaker_list": event.get_speaker_queue()})
            else:
                return JsonResponse({"status": _("Ange ett korrekt kommando.")})
    else:
        return JsonResponse({})


@login_required()
def speaker_list_user_add_self(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user
    speaker_number = EntryAsParticipant.objects.get(event=event, user=user).speech_nr
    event.add_speaker_to_queue(speaker_number)
    messages.success(request,"Du har skrivit upp dig på talarlistan!")
    return redirect(reverse('events:user view', kwargs={'pk': event.pk}))


@login_required()
def speaker_list_user_remove_self(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user
    speaker_number = EntryAsParticipant.objects.get(event=event, user=user).speech_nr
    event.remove_speaker_from_queue(speaker_number)
    return redirect(reverse('events:user view', kwargs={'pk': event.pk}))


@login_required()
def speaker_list_display(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/templates/speaker_list/display_speaker_list.html', {
        'speaker_list': event.get_speaker_queue(), 'event': event
    })


@login_required()
def administer_speaker_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/templates/speaker_list/administer_speaker_list.html', {
        'event': event
    })