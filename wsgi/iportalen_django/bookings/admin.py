from django.contrib import admin
from .models import Bookable, Booking, BookingSlot


class BookingSlotInline(admin.TabularInline):
    model = BookingSlot
    extra = 0

class BookableAdmin(admin.ModelAdmin):
    inlines = [
        BookingSlotInline
    ]

admin.site.register(Bookable, BookableAdmin)
admin.site.register(Booking)
