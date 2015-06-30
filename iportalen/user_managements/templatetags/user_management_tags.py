__author__ = 'jonathan'
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

