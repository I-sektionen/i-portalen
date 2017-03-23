from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Permission, Group
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import IUser, MasterProfile, BachelorProfile, IpikureSubscriber
from utils.admin import iportalen_admin_site, iportalen_superadmin_site
from django.db import models
from django.core.urlresolvers import reverse


def persons(self):
    return ', '.join(['<a href="{url}">{name}</a>'.format(
        url=reverse('iportalenadmin:user_managements_iuser_change', args=(x.pk,)),
        name=x.username) for x in self.user_set.all().order_by('username')])

persons.allow_tags = True


def groups(self):
    return ', '.join(['<a href="{url}">{name}</a>'.format(
        url=reverse('iportalenadmin:auth_group_change', args=(x.pk,)),
        name=x.name) for x in self.group_set.all().order_by('name')])

groups.allow_tags = True


class CustomPermission(admin.ModelAdmin):
    list_display = ['name', groups]
    list_display_links = ['name']


class CustomGroup(GroupAdmin):
    list_display = ['name', persons]
    list_display_links = ['name']
    formfield_overrides = {models.ManyToManyField: {'widget': FilteredSelectMultiple("Rättigheter", is_stacked=False)}, }


class IUserAdmin(UserAdmin):
    @staticmethod
    def show_kobra_url(obj):
        return '<a href="{:}" target="_blank">Uppdatera från kobra</a>'.format(obj.update_from_kobra_url)

    show_kobra_url.allow_tags = True

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_superuser', "show_kobra_url")
    list_filter = ('groups', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': (
            'username',
            'password',
            'first_name',
            'last_name',
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


iportalen_admin_site.unregister(Group)
iportalen_admin_site.register(Group, CustomGroup)
iportalen_admin_site.register(IUser, IUserAdmin)
iportalen_admin_site.register(MasterProfile)
iportalen_admin_site.register(BachelorProfile)
iportalen_admin_site.register(Permission, CustomPermission)
iportalen_admin_site.register(IpikureSubscriber)

iportalen_superadmin_site.register(IUser)
iportalen_superadmin_site.register(MasterProfile)
iportalen_superadmin_site.register(BachelorProfile)
iportalen_superadmin_site.register(Permission)
iportalen_superadmin_site.register(IpikureSubscriber)
