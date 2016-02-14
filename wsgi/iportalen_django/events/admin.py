from django.contrib import admin
from .models import Event, EntryAsPreRegistered, EntryAsReserve, EntryAsParticipant, OtherAttachment, ImageAttachment
from utils.admin import iportalen_admin_site, HiddenModelAdmin


class OtherAttachmentInline(admin.StackedInline):
    model = OtherAttachment
    readonly_fields = ('file_name', 'file')
    extra = 0


class OtherAttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('file_name', 'modified_by')
    list_display = ('event', 'file_name')
    list_filter = ('event',)


class ImageAttachmentInline(admin.TabularInline):
    model = ImageAttachment
    readonly_fields = ('img', 'thumbnail')
    extra = 0


class ImageAttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('thumbnail', 'modified_by')
    list_display = ('event',)
    list_filter = ('event',)


class EventAdmin(HiddenModelAdmin):
    inlines = [OtherAttachmentInline, ImageAttachmentInline]

iportalen_admin_site.register(ImageAttachment, ImageAttachmentAdmin)
iportalen_admin_site.register(OtherAttachment, OtherAttachmentAdmin)
iportalen_admin_site.register(Event)
iportalen_admin_site.register(EntryAsPreRegistered)
iportalen_admin_site.register(EntryAsReserve)
iportalen_admin_site.register(EntryAsParticipant)
