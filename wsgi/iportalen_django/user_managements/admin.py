from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import IUser, MasterProfile, BachelorProfile


class IUserAdmin(UserAdmin):
    def show_kobra_url(self, obj):
        return '<a href="%s" target="_blank">Uppdatera från kobra</a>' % (obj.update_from_kobra_url)
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
            'expected_exam_year',
            'bachelor_profile',
            'master_profile',
            'groups',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
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

admin.site.register(IUser, IUserAdmin)
admin.site.register(MasterProfile)
admin.site.register(BachelorProfile)
admin.site.register(Permission)
