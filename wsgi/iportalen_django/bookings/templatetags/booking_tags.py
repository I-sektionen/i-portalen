__author__ = 'isac'
from django.template.loader_tags import register

from bookings.models import Bookable

@register.assignment_tag()
def get_all_bookables():
    bookables = Bookable.objects.all()
    print("hej")
    print(bookables)
    return bookables