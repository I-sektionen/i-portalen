from django.contrib import admin
from .models import Article, OtherAttachment, ImageAttachment
from utils.admin import HiddenModelAdmin, iportalen_admin_site, iportalen_superadmin_site


class OtherAttachmentInline(admin.StackedInline):
    model = OtherAttachment
    readonly_fields = ('file_name', 'file')
    extra = 0


class OtherAttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('file_name', 'modified_by')
    list_display = ('article', 'file_name')
    list_filter = ('article',)


class ImageAttachmentInline(admin.TabularInline):
    model = ImageAttachment
    readonly_fields = ('img', 'thumbnail')
    extra = 0


class ImageAttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('thumbnail', 'modified_by')
    list_display = ('article',)
    list_filter = ('article',)


class ArticleAdmin(HiddenModelAdmin):
    inlines = [OtherAttachmentInline, ImageAttachmentInline]

iportalen_admin_site.register(ImageAttachment, ImageAttachmentAdmin)
iportalen_admin_site.register(Article, ArticleAdmin)
iportalen_admin_site.register(OtherAttachment, OtherAttachmentAdmin)

iportalen_superadmin_site.register(ImageAttachment)
iportalen_superadmin_site.register(Article)
iportalen_superadmin_site.register(OtherAttachment)
