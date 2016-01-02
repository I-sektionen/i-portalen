from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from bookings.models import Bookable


@register.assignment_tag()
def get_all_bookables():
    bookables = Bookable.objects.all()
    return bookables


@register.assignment_tag
def get_menu_choices_bookings(user):
    menu_choices = []
    if user.has_perm("bookings.add_invoice"):
        menu_choices.append(("Administrera bokningar", reverse('admin:app_list', args=('bookings',))))
    return menu_choices