from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from django.utils.translation import ugettext as _


@register.assignment_tag
def can_vote(question, user):
    return question.can_vote(user)


@register.assignment_tag
def show_result(question, user):
    return question.show_result(user)


@register.assignment_tag
def get_menu_choices_user(user):
    menu_choices = []

    #if user.has_perm("user_managements.add_iuser"):
    menu_choices.append((_("Skapa en omröstning"), reverse('votings:create')))

    return menu_choices