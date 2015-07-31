from django.contrib import admin
from .models import Bookable, Booking, BookingSlot, UserInvoice, CustomInvoice, VariableCostAmount,\
    VariableCostTemplate, FixedCostTemplate


class BookingSlotInline(admin.TabularInline):
    model = BookingSlot
    extra = 0


class BookableAdmin(admin.ModelAdmin):
    inlines = [
        BookingSlotInline
    ]


class

admin.site.register(Bookable, BookableAdmin)
admin.site.register(Booking)
admin.site.register(UserInvoice)
admin.site.register(CustomInvoice)
admin.site.register(VariableCostTemplate)
admin.site.register(FixedCostTemplate)
