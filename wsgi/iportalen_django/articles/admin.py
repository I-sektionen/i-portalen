from django.contrib import admin
from .models import Article, OtherAttachment, ImageAttachment
from utils.admin import HiddenModelAdmin, iportalen_admin_site
from django.contrib.admin import ModelAdmin


class OtherAttachmentInline(admin.StackedInline):
    model = OtherAttachment


#class ArticleAdmin(HiddenModelAdmin):


iportalen_admin_site.register(ImageAttachment, HiddenModelAdmin)
iportalen_admin_site.register(Article, HiddenModelAdmin)
iportalen_admin_site.register(OtherAttachment, HiddenModelAdmin)
