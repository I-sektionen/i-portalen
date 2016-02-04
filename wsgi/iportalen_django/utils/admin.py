from django.contrib import admin
from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active

iportalen_admin_site = MyAdminSite(name='iportalenadmin')


class HiddenModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
