from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from django.utils.translation import ugettext as _


@register.assignment_tag
def get_menu_choices_faq(user):
    menu_choices = []

    if user.has_perm('faq.add_question'):
        menu_choices.append((_("Administrera FAQ"), reverse('admin:app_list', args=('faq',))))

    return menu_choices
