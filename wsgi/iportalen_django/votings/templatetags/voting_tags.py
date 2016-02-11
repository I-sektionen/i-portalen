from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from django.utils.translation import ugettext as _
from votings.models import QuestionGroup


@register.assignment_tag
def can_vote(question, user):
    return question.can_vote(user)


@register.assignment_tag
def show_result(question, user):
    return question.show_result(user)


@register.assignment_tag
def detailed(question, user):
    return question.detailed(user)

@register.assignment_tag
def get_menu_choices_user(user):
    menu_choices = []

    if user.has_perm("votings.add_questiongroup"):
        menu_choices.append((_("Skapa en omröstning"), reverse('votings:create')))

    return menu_choices


@register.simple_tag
def percent_of_votes(votes, voters):
    return "{percent}%".format(percent=round(((votes/voters)*100), 2))


@register.assignment_tag
def get_questions(event):
    qg = QuestionGroup.objects.published().get(event=event)
    return qg