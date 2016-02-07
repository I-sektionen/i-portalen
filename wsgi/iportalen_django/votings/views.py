from django.shortcuts import render, get_object_or_404

from votings.models import QuestionGroup, Question


def votings(request):
    qg = QuestionGroup.objects.published()
    return render(request, "votings/votings.html", {"question_groups": qg})


def question_group(request, qg_pk):
    qg = get_object_or_404(QuestionGroup, pk=qg_pk)
    return render(request, "votings/question_group.html", {"question_group": qg})


def question_details(request):
    return None


def question_result(request):
    return None