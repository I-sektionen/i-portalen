from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from user_managements.models import BachelorProfile, MasterProfile, IUser


@register.assignment_tag
def get_all_users():
    users = IUser.objects.filter(
        is_active=True,
    ).order_by('name')
    return users


@register.assignment_tag
def get_user(liuid):
    user = IUser.objects.get(username=liuid)
    return user


@register.assignment_tag
def get_bachelor_profiles():
    profiles = BachelorProfile.objects.all().order_by('name')
    return profiles


@register.assignment_tag
def get_master_profiles():
    profiles = MasterProfile.objects.all().order_by('name')
    return profiles

@register.assignment_tag
def get_menu_choices_user(user):
    menu_choices = []

    if user.has_perm("user_managements.add_iuser"):
        menu_choices.append(("Lägg till Liu-idn i whitelist", reverse('add users to whitelist')))

    if user.has_perm('user_managements.can_view_users'):
        menu_choices.append(('Alla användare', reverse('all users')))

    if user.has_perm('user_managements.can_view_subscribers'):
        menu_choices.append(('Lista Ipikuréprenumeranter', reverse('ipikure_subscribers')))


    return menu_choices