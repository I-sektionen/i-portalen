from django.contrib import admin
from django.db.models.aggregates import Max, Min
from django.utils.safestring import mark_safe
from .models import (
    Bookable,
    Booking,
    BookingSlot,
    VariableCostAmount,
    Invoice,
    VariableCostTemplate,
    FixedCostTemplate,
    PartialBooking,
    FixedCostAmount
)
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from utils.admin import iportalen_admin_site, iportalen_superadmin_site


class BookingSlotInline(admin.TabularInline):
    model = BookingSlot
    extra = 0
    ordering = ("start_time",)


class BookableAdmin(admin.ModelAdmin):
    inlines = [
        BookingSlotInline
    ]


class PartialBookingsInline(admin.TabularInline):
    model = PartialBooking
    extra = 1


class InvoiceInline(admin.TabularInline):
    model = Invoice
    show_change_link = True
    extra = 0
    max_num = 0  # So we don't show the 'add another' link.
    can_delete = False
    readonly_fields = ('ocr', 'due', 'status')


def _get_invoice_status_display(obj):
    try:
        inv = Invoice.objects.get(booking=obj)
        return inv.get_status_display()
    except MultipleObjectsReturned:
        return _("Flera fakturor existerar")
    except ObjectDoesNotExist:
        return _("Ej skapad.")


class BookingsAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(BookingsAdmin, self).get_queryset(request)
        return qs.annotate(start = Min("bookings__date")).order_by("-start")

    @staticmethod
    def link_to_user(obj):
        return mark_safe("<a href={url} target='_blank'>{name}, {phone}</a>".format(
            url=obj.user.get_absolute_url(), name=obj.user.get_full_name, phone=obj.user.phone))
    link_to_user.allow_tags = True
    link_to_user.short_description = _("Länk till användaren")

    def has_add_permission(self, request):
        return False

    list_display = ('user', 'link_to_user', 'bookable', 'start_time', _get_invoice_status_display,)
    readonly_fields = ('create_invoice_url', _get_invoice_status_display)

    @staticmethod
    def create_invoice_url(obj):
        s = reverse("bookings:create custom invoice", args=[obj.pk])
        return "<a href=\"{url}\">{text}</a>".format(url=s, text=_("Skapa/Se befintlig"))

    create_invoice_url.allow_tags = True
    create_invoice_url.short_description = _("Länk till faktura")

    _get_invoice_status_display.short_description = _("Status på faktura")

    list_filter = ('bookable', )
    search_fields = ('user', )
    inlines = [
        PartialBookingsInline,
        InvoiceInline
    ]


class VariableCostInline(admin.TabularInline):
    model = VariableCostAmount
    extra = 1


class FixedCostInline(admin.TabularInline):
    model = FixedCostAmount
    extra = 1


class UserInvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('ocr', 'send_invoice_email')
    # fields = ('status', 'due', 'booking')

    @staticmethod
    def send_invoice_email(obj):
        try:
            s = reverse("bookings:send invoice email", args=[obj.pk])
            return "<a href=\"{url}\">{text}</a>".format(url=s, text=_("Skicka email till användare"))
        except:
            return _("Ej tillgängligt")
    send_invoice_email.short_description = _("Skicka faktura")
    send_invoice_email.allow_tags = True

    inlines = [
        VariableCostInline,
        FixedCostInline,
    ]

    search_fields = ('ocr',)
    list_filter = ('status', )
    list_display = ('ocr', 'due', 'status')


iportalen_admin_site.register(Bookable, BookableAdmin)
iportalen_admin_site.register(Booking, BookingsAdmin)

iportalen_admin_site.register(Invoice, UserInvoiceAdmin)

iportalen_admin_site.register(VariableCostTemplate)
iportalen_admin_site.register(FixedCostTemplate)


iportalen_superadmin_site.register(Bookable)
iportalen_superadmin_site.register(Booking)
iportalen_superadmin_site.register(Invoice)
iportalen_superadmin_site.register(VariableCostTemplate)
iportalen_superadmin_site.register(FixedCostTemplate)
