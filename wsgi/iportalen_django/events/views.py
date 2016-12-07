from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
import csv
from utils.validators import liu_id_validator
from .forms import EventForm, CheckForm, ImportEntriesForm, RejectionForm, AttachmentForm, \
    ImageAttachmentForm, DeleteForm
from .models import Event, EntryAsPreRegistered, EntryAsReserve, EntryAsParticipant, OtherAttachment, \
    ImageAttachment
from .exceptions import CouldNotRegisterException
from user_managements.models import IUser
from django.utils.translation import ugettext as _

# Create your views here.
from wsgi.iportalen_django.iportalen import settings
from utils.time import six_months_back


@login_required()
def summarise_noshow(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if not event.can_administer(request.user):
        raise PermissionDenied
    if not event.finished:
        event.finished = True
    noshows = event.no_show
    for user in noshows:
        noshow = EntryAsPreRegistered.objects.get(event=event, user=user)
        noshow.no_show = True
        noshow.save()
    for user in noshows:
        if len(EntryAsPreRegistered.objects.get_noshow(user=user)) == 2:
            subject = "Du har nu missat ditt andra event"
            body = "<p>Hej du har missat 2 event som du har anmält dig på. Om du missar en tredje gång så blir vi tvungna att stänga av dig från " \
                   "framtida event fram tills ett halv år framåt.</p>"
            send_mail(subject, "", settings.EMAIL_HOST_USER, [user.email, ], fail_silently=False, html_message=body)
        elif len(EntryAsPreRegistered.objects.get_noshow(user=user)) == 3:
            subject = "Du har nu missat ditt tredje event"
            body = "<p>Hej igen du har missat 3 event som du har anmält dig på. Du kommer härmed att blir avstängd från " \
                   "framtida event fram tills ett halv år framåt. Ha en bra dag :)</p>"
            send_mail(subject, "", settings.EMAIL_HOST_USER, [user.email, ], fail_silently=False, html_message=body)
    event.save()
    return redirect("events:administer event", pk=pk)


def view_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if (event.status == Event.APPROVED and event.show_event_before_experation) or event.can_administer(request.user):
        return render(request, "events/event.html", {"event": event})
    raise PermissionDenied


@login_required()
def register_to_event(request, pk):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        try:
            event.register_user(request.user)
            messages.success(request, _("Du är nu registrerad på eventet."))
        except CouldNotRegisterException as err:
            messages.error(request,
                           _("Fel, kunde inte registrera dig på ") + err.event.headline + _(" för att ") + err.reason + ".")
    return redirect("events:event", pk=pk)


@login_required()
@transaction.atomic
def import_registrations(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.can_administer(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        form = ImportEntriesForm(request.POST)
        if form.is_valid():
            list_of_liu_id = form.cleaned_data['users'].splitlines()
            for liu_id in list_of_liu_id:
                try:
                    event.register_user(IUser.objects.get(username=liu_id))
                except CouldNotRegisterException as err:
                    messages.error(
                        request,
                        "".join([_("Fel, kunde inte registrera"),
                                 " {liu_id} ",
                                 _("på"),
                                 " {hedline} ",
                                 _("för att"),
                                 " {reason}."]).format(
                            liu_id=liu_id,
                            hedline=err.event.headline,
                            reason=err.reason))
                except ObjectDoesNotExist:
                    messages.error(request, "".join(["{liu_id} ", _("finns inte i databasen.")]).format(liu_id))
    else:
        form = ImportEntriesForm()
    return render(request, "events/import_users.html", {'form': form})


@login_required()
def register_as_reserve(request, pk):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        entry = event.register_reserve(request.user)
        messages.success(request,
                         _("Du är nu anmäld som reserv på eventet, du har plats nr. ") + str(entry.position()) + ".")
    return redirect("events:event", pk=pk)


@login_required()
def administer_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = DeleteForm(request.POST or None, request.FILES or None,)
    if event.can_administer(request.user):
        return render(request, 'events/administer_event.html', {
            'event': event, 'form':form,
        })
    else:
        raise PermissionDenied  # Nope.


@login_required()
def preregistrations_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/event_preregistrations.html', {
            'event': event,
        })
    else:
        raise PermissionDenied  # Nope.


@login_required()
def participants_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/event_participants.html', {
            'event': event,
        })
    else:
        raise PermissionDenied  # Nope.


@login_required()
def speech_nr_list(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.can_administer(request.user):
        return render(request, 'events/event_speech_nr_list.html', {
            'event': event,
        })
    else:
        raise PermissionDenied  # Nope.


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
        raise PermissionDenied  # Nope.


@login_required()
def check_in(request, pk):  # TODO: Reduce complexity
    event = get_object_or_404(Event, pk=pk)
    can_administer = event.can_administer(request.user)
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            form_user = form.cleaned_data["user"]
            try:
                liu_id_validator(form_user)
                is_liu_id = True
            except:
                is_liu_id = False

            try:
                if is_liu_id:
                    event_user = IUser.objects.get(username=form_user)
                else:
                    event_user = IUser.objects.get(rfid_number=form_user)
            except ObjectDoesNotExist:
                messages.error(request, _("Användaren finns inte i databasen"))
                form = CheckForm()
                return render(request, 'events/event_check_in.html', {
                    'form': form, 'event': event, "can_administer": can_administer,
                })
            if event_user in event.preregistrations or form.cleaned_data["force_check_in"]:
                try:
                    event.check_in(event_user)
                    if event.extra_deadline:
                        try:
                            extra = event.entryaspreregistered_set.get(user=event_user).timestamp < event.extra_deadline
                        except:
                            extra = False
                        if extra:
                            extra_str = _("<br>Anmälde sig i tid för att ") + event.extra_deadline_text + "."
                        else:
                            extra_str = _("<br><span class='errorlist'>Anmälde sig ej i tid för att ") + \
                                        event.extra_deadline_text + ".</span>"
                    else:
                        extra_str = ""
                    messages.success(request, "".join(["{0} {1} ",
                                                       _("checkades in med talarnummer:"),
                                                       " {2}{3}"]).format(
                        event_user.first_name.capitalize(),
                        event_user.last_name.capitalize(),
                        event.entryasparticipant_set.get(user=event_user).speech_nr,
                        extra_str
                    ), extra_tags='safe')
                    form = CheckForm()
                    return render(request, 'events/event_check_in.html', {
                        'form': form, 'event': event, "can_administer": can_administer,
                    })
                except:
                    messages.error(request, "".join(["{0} {1} ",_("är redan incheckad")]).format(
                        event_user.first_name.capitalize(), event_user.last_name.capitalize()))

            else:
                if event_user in event.reserves:
                    messages.error(
                        request,
                        "".join(["{0} {1} ", _("är anmäld som reserv")]).format(
                            event_user.first_name.capitalize(), event_user.last_name.capitalize()))
                else:
                    messages.error(request, "".join(["{0} {1} ", _("är inte anmäld på eventet")]).format(
                        event_user.first_name.capitalize(), event_user.last_name.capitalize()))
                reserve = True
                return render(request, 'events/event_check_in.html',
                              {'form': form, 'event': event, 'reserve': reserve, "can_administer": can_administer, })

        else:
            return render(request, 'events/event_check_in.html', {
                'form': form, 'event': event, "can_administer": can_administer,
            })

    form = CheckForm()
    return render(request, 'events/event_check_in.html', {
        'form': form, 'event': event, "can_administer": can_administer,
    })


@login_required()
def all_unapproved_events(request):
    if request.user.has_perm("events.can_approve_event"):
        events = Event.objects.filter(status=Event.BEING_REVIEWED, end__gte=timezone.now())
        events_to_delete = Event.objects.filter(status=Event.BEING_CANCELD, end__gte=timezone.now())
        return render(request, 'events/approve_event.html', {'events': events, 'events_to_delete': events_to_delete})
    else:
        raise PermissionDenied


@login_required()
@transaction.atomic
def approve_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.approve(request.user):
        return redirect(reverse('events:unapproved'))
    else:
        raise PermissionDenied


@login_required()
def unapprove_event(request, pk):
    event = Event.objects.get(pk=pk)
    form = RejectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if event.reject(request.user, form.cleaned_data['rejection_message']):
                messages.success(request, _("Eventet har avslagits."))
                return redirect('events:unapproved')
            else:
                raise PermissionDenied
    return render(request, 'events/reject.html', {'form': form, 'event': event})


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
            messages.success(request, _("Du är nu avregistrerad på eventet."))
        except CouldNotRegisterException as err:
            messages.error(request,
                           "".join([_("Fel, kunde inte avregistrera dig på "),
                                    err.event.headline,
                                    _(" för att "),
                                    err.reason,
                                    "."]))
    return redirect("events:event", pk=pk)


def event_calender(request):
    return render(request, "events/calender.html")


def event_calender_view(request):
    events = Event.objects.published().order_by('start')
    return render(request, "events/calendar_view.html", {'events': events})


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
    user_events = Event.objects.user(request.user)
    return render(request, 'events/my_events.html', {
        'user_events': user_events
    })


@login_required()
def create_or_modify_event(request, pk=None):  # TODO: Reduce complexity
    if pk:  # if pk is set we modify an existing event.
        duplicates = Event.objects.filter(replacing_id=pk)
        if duplicates:
            links = ""
            for d in duplicates:
                links += "<a href='{0}'>{1}</a><br>".format(d.get_absolute_url(), d.headline)
            messages.error(request,
                           "".join([_("Det finns redan en ändrad version av det här arrangemanget! "
                                      "Är du säker på att du vill ändra den här?<br>"
                                      "Följande ändringar är redan föreslagna: <br> "),
                                    "{:}"]).format(links),
                           extra_tags='safe')
        event = get_object_or_404(Event, pk=pk)
        if not event.can_administer(request.user):
            raise PermissionDenied
        form = EventForm(request.POST or None, request.FILES or None, instance=event)
    else:  # new event.
        form = EventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)

            if form.cleaned_data['draft']:
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
            if event.status == Event.DRAFT:
                messages.success(request, _("Dina ändringar har sparats i ett utkast."))
            elif event.status == Event.BEING_REVIEWED:
                body = "<h1>Hej!</h1><br><br><p>Det finns nya artiklar att godkänna på i-Portalen.<br><a href='https://www.i-portalen.se/article/unapproved/'>Klicka här!</a></p><br><br><p>Med vänliga hälsningar, <br><br>Admins @ webgroup"
                send_mail('Ny artikel att godkänna', '', settings.EMAIL_HOST_USER, ['utgivare@isektionen.se'], fail_silently=False, html_message=body)
                messages.success(request, _("Dina ändringar har skickats för granskning."))
            return redirect('events:by user')
        else:
            messages.error(request, _("Det uppstod ett fel, se detaljer nedan."))
            return render(request, 'events/create_event.html', {
                'form': form,
            })
    return render(request, 'events/create_event.html', {
        'form': form,
    })


def upload_attachments(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.can_administer(request.user):
        raise PermissionDenied
    AttachmentFormset = modelformset_factory(OtherAttachment,
                                             form=AttachmentForm,
                                             max_num=30,
                                             extra=3,
                                             can_delete=True,
                                             )
    if request.method == 'POST':
        formset = AttachmentFormset(request.POST, request.FILES, queryset=OtherAttachment.objects.filter(event=event))
        if formset.is_valid():
            for entry in formset.cleaned_data:
                if not entry == {}:
                    if entry['DELETE']:
                        entry['id'].delete()  # TODO: Remove the clear option from html-widget (or make it work).
                    else:
                        if entry['id']:
                            attachment = entry['id']
                        else:
                            attachment = OtherAttachment(event=event)
                            attachment.file_name = entry['file'].name
                        attachment.file = entry['file']
                        attachment.display_name = entry['display_name']
                        attachment.modified_by = request.user
                        attachment.save()
            messages.success(request, 'Dina bilagor har sparats.')
            return redirect('events:manage attachments', pk=event.pk)
        else:
            return render(request, "events/attachments.html", {
                        'event': event,
                        'formset': formset,
                        })
    formset = AttachmentFormset(queryset=OtherAttachment.objects.filter(event=event))
    return render(request, "events/attachments.html", {
                        'event': event,
                        'formset': formset,
                        })


@login_required()
def upload_attachments_images(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.can_administer(request.user):
        raise PermissionDenied
    AttachmentFormset = modelformset_factory(ImageAttachment,
                                             form=ImageAttachmentForm,
                                             max_num=30,
                                             extra=3,
                                             can_delete=True,
                                             )
    if request.method == 'POST':
        formset = AttachmentFormset(request.POST,
                                    request.FILES,
                                    queryset=ImageAttachment.objects.filter(event=event)
                                    )
        if formset.is_valid():
            for entry in formset.cleaned_data:
                if not entry == {}:
                    if entry['DELETE']:
                        entry['id'].delete()  # TODO: Remove the clear option from html-widget (or make it work).
                    else:
                        if entry['id']:
                            attachment = entry['id']
                        else:
                            attachment = ImageAttachment(event=event)
                        attachment.img = entry['img']
                        attachment.caption = entry['caption']
                        attachment.modified_by = request.user
                        attachment.save()
            messages.success(request, 'Dina bilagor har sparats.')
            return redirect('events:event', event.pk)
        else:
            return render(request, "events/attach_images.html", {
                        'event': event,
                        'formset': formset,
                        })
    formset = AttachmentFormset(queryset=ImageAttachment.objects.filter(event=event))
    return render(request, "events/attach_images.html", {
                        'event': event,
                        'formset': formset,
                        })


@login_required()
def user_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user
    #checks if user is a participant
    try:
        participant = EntryAsParticipant.objects.get(event=event, user=user)
    except EntryAsParticipant.DoesNotExist:
        raise PermissionDenied
    return render(request, "events/user_view.html", {'event': event})


def calendar_feed(request):
    events = Event.objects.published()
    response = render(request,
                      template_name='events/feed.ics',
                      context={'events': events},
                      content_type='text/calendar; charset=UTF-8')
    response['Filename'] = 'feed.ics'
    response['Content-Disposition'] = 'attachment; filename=feed.ics'
    return response


def personal_calendar_feed(request, liu_id):
    u = get_object_or_404(IUser, username=liu_id)
    events = Event.objects.events_by_user(u)
    response = render(request,
                      template_name='events/feed.ics',
                      context={'liu_user': u, 'events': events},
                      content_type='text/calendar; charset=UTF-8')
    response['Filename'] = 'feed.ics'
    response['Content-Disposition'] = 'attachment; filename=feed.ics'
    return response


@login_required()
@permission_required('events.can_view_no_shows')
def show_noshows(request):
    user = request.user
    no_shows = EntryAsPreRegistered.objects.filter(no_show = True, timestamp__gte= six_months_back).order_by("user")
    result = []

    tempuser = {"user": None, "count": 0, "no_shows": []}
    for no_show in no_shows:
        if tempuser["user"] == no_show.user:
            tempuser["count"] += 1
        else:
            if tempuser["user"]:
                result.append(tempuser)
            tempuser = {"user": no_show.user, "count":1, "no_shows": []}

        tempuser["no_shows"].append(no_show)
    if tempuser["user"]:
        result.append(tempuser)

    return render(request, "events/show_noshows.html", {"user": user, "no_shows": result})


@login_required()
@permission_required('events.can_remove_no_shows')
def remove_noshow(request):
    user = request.user
    if request.method == 'POST':
        try:
            user_id=request.POST.get('user_id')
            event_id=request.POST.get('event_id')
        except:
            return JsonResponse({'status': 'fel request'})
        no_shows = EntryAsPreRegistered.objects.filter(user_id=user_id, event_id=event_id, no_show=True)
        print(no_shows)
        if len(no_shows)==1:
            no_shows[0].no_show=False
            no_shows[0].save()
            return JsonResponse({'status': 'OK'})
        elif len(no_shows)==0:
            return JsonResponse({'status': 'Ingen no show hittades'})
        else:
            return JsonResponse({'status': 'Error: fler än ett no show hittades'})

    return JsonResponse({'status': 'fel request'})

@login_required()
def cancel(request, pk=None):
    event = get_object_or_404(Event, pk=pk)
    print('steg1')
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        print('steg2')
        print(form.errors)
        if form.is_valid():
            print('steg3')
            event.status = Event.BEING_CANCELD
            event.cancel_message = form.cleaned_data["cancel"]
            event.save()
            form_user = form.cleaned_data["cancel"]
            body = "<h1>Hej!</h1><br><br><p>Det finns nya event att ställa in på i-Portalen.<br><a href='https://www.i-portalen.se/article/unapproved/'>Klicka här!</a></p><br><br><p>Med vänliga hälsningar, <br><br>Admins @ webgroup" + form_user
            send_mail('Nytt event att ställa in', '', settings.EMAIL_HOST_USER, ['utgivare@isektionen.se'], fail_silently=False, html_message=body)
            messages.success(request, _("Dina ändringar har skickats för granskning."))
        #     vill låsa radera knapp
        else:
            messages.error(request, _("Det har ej fyllts i varför eventet önskas raderas."))
            return redirect("events:administer event", pk=pk)
    #         vill stanna kvar på sidan

    return render(request, 'events/administer_event.html', {'event': event, 'form':form, 'form_user':form_user, })







