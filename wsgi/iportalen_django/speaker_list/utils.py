from django.http import JsonResponse
from .models import SpeakerList
from .exceptions import SpeakerListException
from django.utils.translation import ugettext as _


def add_to_speakerlist(event, speech_nr):
    try:
        user = event.entryasparticipant_set.get(speech_nr=speech_nr).user
        SpeakerList.objects.add(event=event, user=user)
        return JsonResponse({'status': 'ok'})
    except SpeakerListException as e:
        return JsonResponse({"status": str(e.reason)})
    except:
        return JsonResponse({"status": _("Ingen användare med det talarnummret.")})


def next_speaker(event):
    try:
        SpeakerList.objects.next(event=event)
        return JsonResponse({'status': 'ok'})
    except SpeakerListException as e:
        return JsonResponse({"status": str(e.reason)})


def remove_from_speakerlist(event, speech_nr):
    try:
        user = event.entryasparticipant_set.get(speech_nr=speech_nr).user
        SpeakerList.objects.remove(event=event, user=user)
        return JsonResponse({'status': 'ok'})
    except SpeakerListException as e:
        return JsonResponse({"status": str(e.reason)})
    except:
        return JsonResponse({"status": _("Ingen användare med det talarnummret.")})

