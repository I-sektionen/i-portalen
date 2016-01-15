from django.contrib import admin
from .models import Bookable, Booking, BookingSlot, VariableCostAmount, Invoice, \
    VariableCostTemplate, FixedCostTemplate, PartialBooking, FixedCostAmount
from django.core.exceptions import ObjectDoesNotExist
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




class BookingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bookable', 'start_time', '_invoice_status')
    list_filter = ('bookable', '_invoice_status')
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
    # fields = ('invoice_pdf_url', )
    readonly_fields = ('ocr',)
    inlines = [
        VariableCostInline,
        FixedCostInline,
    ]


iportalen_admin_site.register(Bookable, BookableAdmin)
iportalen_admin_site.register(Booking, BookingsAdmin)

iportalen_admin_site.register(Invoice, UserInvoiceAdmin)

iportalen_admin_site.register(VariableCostTemplate)
iportalen_admin_site.register(FixedCostTemplate)
