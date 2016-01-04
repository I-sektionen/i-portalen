from django.core.urlresolvers import reverse
from django.template.loader_tags import register


@register.assignment_tag
def get_menu_choices_course_evaluation(user):
    menu_choices = []

    if user.has_perm('course_evaluations.add_course'):
        menu_choices.append(("Administrera kursutvärderingar", reverse('course_evaluations:admin')))

    return menu_choices