from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Permission, Group
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import IUser, MasterProfile, BachelorProfile, IpikureSubscriber
from utils.admin import HiddenModelAdmin, iportalen_admin_site

class IUserAdmin(UserAdmin):
    def show_kobra_url(self, obj):
        return '<a href="{:}" target="_blank">Uppdatera från kobra</a>'.format(obj.update_from_kobra_url)

    show_kobra_url.allow_tags = True

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_superuser', "show_kobra_url")
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': (
            'username',
            'password',
            'first_name',
            'last_name',
            'p_nr',
            'address',
            'zip_code',
            'city',
            'gender',
            'allergies',
            'start_year',
            'current_year',
            'klass',
            'bachelor_profile',
            'master_profile',
            'groups',
            'rfid_number',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'is_member', 'must_edit')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser')}
         ),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


class UserInline(admin.TabularInline):
    model = Group.user.through
    extra = 0


class CustomGroup(GroupAdmin):
    inlines = [UserInline]


iportalen_admin_site.unregister(Group)
iportalen_admin_site.register(Group, GroupAdmin)
iportalen_admin_site.register(IUser, IUserAdmin)
iportalen_admin_site.register(MasterProfile)
iportalen_admin_site.register(BachelorProfile)
iportalen_admin_site.register(Permission)
iportalen_admin_site.register(IpikureSubscriber)
