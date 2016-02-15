from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from events.models import Event
from votings.exceptions import CouldNotVoteException
from votings.forms import VotingForm
from votings.models import QuestionGroup, Question


@login_required()
def votings(request):
    qg = QuestionGroup.objects.published()
    return render(request, "votings/votings.html", {"question_groups": qg})


@login_required()
def question_group(request, qg_pk):
    qg = get_object_or_404(QuestionGroup, pk=qg_pk)
    return render(request, "votings/question_group.html", {"question_group": qg})


@login_required()
def question_details(request, qg_pk, q_pk):
    q = get_object_or_404(Question, pk=q_pk)
    if not q.can_vote(request.user):
        messages.warning(request, _("Du har redan röstat i den frågan."))
        return redirect(reverse("votings:question group", kwargs={'qg_pk': qg_pk}))
    form = VotingForm(q_pk, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            votes = list(map(int, form.cleaned_data['options']))
            try:
                q.vote(request.user, votes)
                messages.success(request, _("Du har nu röstat, tack för din röst!"))
                return redirect(reverse("votings:question group", kwargs={'qg_pk': qg_pk}))
            except CouldNotVoteException as e:
                messages.error(request, e.reason)
    return render(request, "votings/question_details.html", {"form": form, "question": q})


@login_required()
def question_result(request, qg_pk, q_pk):
    q = get_object_or_404(Question, pk=q_pk)
    return render(request, "votings/result.html", {"question": q})


def create(request):
    return redirect(reverse('iportalenadmin:app_list', args=('votings',)))


@login_required()
def create_from_event(request, event_pk):
    e = get_object_or_404(Event, pk=event_pk)
    if e.can_administer(request.user):
        qg = QuestionGroup.objects.create(name=e.headline,
                                          question_status=QuestionGroup.EVENT,
                                          event=e,
                                          creator=request.user)
        return redirect(reverse('iportalenadmin:votings_questiongroup_change', args=(qg.pk,)))
    else:
        raise PermissionDenied()


def admin_from_event(request, event_pk):
    e = get_object_or_404(Event, pk=event_pk)
    if e.can_administer(request.user):
        qg = get_object_or_404(QuestionGroup, event_id=event_pk)
        return redirect(reverse('iportalenadmin:votings_questiongroup_change', args=(qg.pk,)))
    else:
        raise PermissionDenied()


def get_from_event(request, event_pk):
    qg = get_object_or_404(QuestionGroup, event_id=event_pk)
    return redirect(reverse('votings:question group', args=(qg.pk,)))