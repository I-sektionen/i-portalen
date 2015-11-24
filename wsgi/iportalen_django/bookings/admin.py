from django.contrib import admin
from .models import Bookable, Booking, BookingSlot, VariableCostAmount, Invoice, \
    VariableCostTemplate, FixedCostTemplate, PartialBooking, FixedCostAmount


class BookingSlotInline(admin.TabularInline):
    model = BookingSlot
    extra = 0
    ordering = ("start_time", )

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

    #fields = ('invoice_pdf_url', )

    #invoice_pdf_url.allow_tags = True
    #invoice_pdf_url.short_description = 'Länk till PDF fakturan.'


    inlines = [
        VariableCostInline,
        FixedCostInline,
    ]

admin.site.register(Bookable, BookableAdmin)
admin.site.register(Booking, BookingsAdmin)

admin.site.register(Invoice, UserInvoiceAdmin)

admin.site.register(VariableCostTemplate)
admin.site.register(FixedCostTemplate)
