from django.contrib import admin
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
from utils.admin import iportalen_admin_site


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
        return "Flera fakturor existerar"
    except ObjectDoesNotExist:
        return "Ej skapad."


class BookingsAdmin(admin.ModelAdmin):

    def link_to_user(self, obj):
        return "<a href={url} target='_blank'>{name}, {phone}</a>".format(
            url=obj.user.get_absolute_url(), name=obj.user.get_full_name, phone=obj.user.phone)
    link_to_user.allow_tags = True
    link_to_user.short_description = "Länk till användaren"

    def has_add_permission(self, request):
        return False

    list_display = ('user', 'link_to_user', 'bookable', 'start_time', _get_invoice_status_display,)
    readonly_fields = ('create_invoice_url', _get_invoice_status_display)

    def create_invoice_url(self, obj):
        s = reverse("bookings:create custom invoice", args=[obj.pk])
        return "<a href=\"%s\">Skapa/Se befintlig</a>" % (s,)

    create_invoice_url.allow_tags = True
    create_invoice_url.short_description = "Länk till faktura"

    _get_invoice_status_display.short_description = "Status på faktura"

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

    def send_invoice_email(self, obj):
        try:
            s = reverse("bookings:send invoice email", args=[obj.pk])
            return "<a href=\"%s\">Skicka email till användare</a>" % (s,)
        except:
            return "Ej tillgängligt"
    send_invoice_email.short_description = "Skicka faktura"
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
