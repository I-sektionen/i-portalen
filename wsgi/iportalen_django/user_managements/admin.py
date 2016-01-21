from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Permission, Group
from django.utils.safestring import mark_safe
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import IUser, MasterProfile, BachelorProfile, IpikureSubscriber
from utils.admin import HiddenModelAdmin, iportalen_admin_site


def roles(self):
    #short_name = unicode # function to get group name
    short_name = lambda x: x[:1].upper()  # first letter of a group
    p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x)) for x in self.groups.all()])
    if self.user_permissions.count(): p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)
roles.allow_tags = True
roles.short_description = u'Groups'


def adm(self):
    return self.is_superuser
adm.boolean = True
adm.admin_order_field = 'is_superuser'


def staff(self):
    return self.is_staff
staff.boolean = True
staff.admin_order_field = 'is_staff'


from django.core.urlresolvers import reverse
def persons(self):
    return ', '.join(['<a href="{url}">{name}</a>'.format(url=reverse('admin:user_managements_iuser_change', args=(x.pk,)), name=x.username) for x in self.user_set.all().order_by('username')])
persons.allow_tags = True


class CustomGroup(GroupAdmin):
    list_display = ['name', persons]
    list_display_links = ['name']


class IUserAdmin(UserAdmin):
    def show_kobra_url(self, obj):
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


iportalen_admin_site.unregister(Group)
iportalen_admin_site.register(Group, CustomGroup)
iportalen_admin_site.register(IUser, IUserAdmin)
iportalen_admin_site.register(MasterProfile)
iportalen_admin_site.register(BachelorProfile)
iportalen_admin_site.register(Permission)
iportalen_admin_site.register(IpikureSubscriber)
