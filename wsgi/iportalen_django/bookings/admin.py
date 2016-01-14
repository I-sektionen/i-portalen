from django.contrib import admin
from .models import Bookable, Booking, BookingSlot, VariableCostAmount, Invoice, \
    VariableCostTemplate, FixedCostTemplate, PartialBooking, FixedCostAmount
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


class BookingsAdmin(admin.ModelAdmin):
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

    # invoice_pdf_url.allow_tags = True
    # invoice_pdf_url.short_description = 'Länk till PDF fakturan.'

    inlines = [
        VariableCostInline,
        FixedCostInline,
    ]


iportalen_admin_site.register(Bookable, BookableAdmin)
iportalen_admin_site.register(Booking, BookingsAdmin)

iportalen_admin_site.register(Invoice, UserInvoiceAdmin)

iportalen_admin_site.register(VariableCostTemplate)
iportalen_admin_site.register(FixedCostTemplate)
