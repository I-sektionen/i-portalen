from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .forms import ChangeUserInfoForm, AddWhiteListForm
from .models import IUser
from django.core.urlresolvers import reverse
from django.contrib import messages
from utils.text import random_string_generator
from django.contrib.auth.views import (
    password_reset_confirm,
    password_reset,
)
from utils.kobra import get_user_by_liu_id, LiuGetterError, LiuNotFoundError


def logout_view(request):
    logout(request)
    return redirect('/')  # TODO: Where should this redirect?

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username.lower(), password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                not_member = False
                if user.last_login is None:
                    not_member = True
                auth_login(request, user)
                if not_member:
                    user.is_active = False
                    try:
                        kobra_dict = get_user_by_liu_id(user.username)
                        user.email = kobra_dict['email'].lower()
                        user.last_name = kobra_dict['last_name'].lower()
                        user.first_name = kobra_dict['first_name'].lower()
                        user.rfid_number = kobra_dict['rfid_number']
                        user.p_nr = kobra_dict['personal_number']
                        user.save()
                    except:
                        pass
                    user.save()
                    return render(request, "user_managements/membership.html")
                try:
                    return redirect(request.GET['next'])
                except:
                    return redirect('/')
            else:
                messages.error(request, "Lösenordet är korrekt, men kontot är avstängt! Om detta inte bör vara fallet var god kontakta info@isektionen.se")
                return render(request, "user_managements/login.html")
                # The password is valid, but the account has been disabled!
        else:
            # the authentication system was unable to verify the username and password
            messages.error(request, "Fel Liu-id eller lösenord.")
            return render(request, "user_managements/login.html")
    else:
        return render(request, "user_managements/login.html")


@login_required()
def my_page_view(request):
    return render(request, "user_managements/mypage.html")

@login_required()
def change_user_info_view(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
        return redirect(reverse("mypage_view"))
    else:
        form = ChangeUserInfoForm(instance=user)
        return render(request, "user_managements/user_info_form.html", {'form':form})

@login_required()
@transaction.atomic
def add_users_to_white_list(request):
    user = request.user
    if not user.has_perm("user_managements.add_iuser"):
        raise PermissionDenied
    if request.method == 'POST':
        form = AddWhiteListForm(request.POST)
        if form.is_valid():
            list_of_liu_id = form.cleaned_data['users'].splitlines()
            errors = False

            for liu_id in list_of_liu_id:
                temp_user = IUser(username=liu_id.lower(), email=liu_id.lower()+"@student.liu.se")
                temp_user.set_password(random_string_generator())
                try:
                    temp_user.validate_unique()
                except ValidationError:
                    messages.info(
                        request,
                        "Det finns redan en användare med Liu-id: {:}. Användaren har inte ändrats.".format(liu_id))
                    continue
                try:
                    temp_user.clean_fields()
                    temp_user.clean()
                except ValidationError as e:
                    errors = True
                    str_error = ""
                    for m in e.messages:
                        str_error = str_error + " " + m
                    messages.error(
                        request,
                        "Det uppstod ett fel för användaren med Liu-id: {:}.\n{:}".format(liu_id, str_error))
                    continue
                temp_user.save()
            if errors:
                messages.info(request, "De användare utan fel har skapats och kan nu återställa sitt lösenord.")
            else:
                messages.success(request, "De nya användarna har skapats och kan nu återställa sitt lösenord")
    else:
        form = AddWhiteListForm()
    return render(request, "user_managements/add_whitelist.html", {'form':form})


def set_user_as_member(request):
    request.user.is_active = True
    request.user.save()
    return redirect("/")


def reset(request):
    return password_reset(request, template_name='user_managements/reset/pw_res.html',
                          email_template_name='user_managements/reset/pw_res_email.html',
                          subject_template_name='user_managements/reset/pw_res_email_subject.txt',)


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='user_managements/reset/pw_res_confirm.html',
                                  uidb64=uidb64,
                                  token=token,
                                  post_reset_redirect=reverse('front page'))

def reset_done(request):
    # return password_reset_done(request, template_name='user_managements/reset/pw_res_done.html')
    messages.info(request, "Ett mail kommer inom kort skickas till mailadressen som angavs. I den finns en länk för att skapa ett nytt lösenord.")
    return redirect("/")

def reset_complete(request):
    messages.info(request, "Du har ett nytt lösenord, testa det.")
    return redirect(reverse("login_view"))

@login_required()
def update_user_from_kobra(request, liu_id):
    if not request.user.has_perm("user_managements.add_iuser"):
        messages.error(request, "Du har inte rätt behörighet att updatera från kobra.")
        return render(request, "user_managements/kobra.html")
    try:
        user = IUser.objects.get(username=liu_id)
        kobra_dict = get_user_by_liu_id(liu_id)
        user.email = kobra_dict['email'].lower()
        user.last_name = kobra_dict['last_name'].lower()
        user.first_name = kobra_dict['first_name'].lower()
        user.rfid_number = kobra_dict['rfid_number']
        user.p_nr = kobra_dict['personal_number']
        user.save()
        messages.info(request, "{:} har uppdaterats i databasen.".format(liu_id))
    except IUser.DoesNotExist:
        messages.error(request, "Personen finns inte i systemet.")
    except LiuNotFoundError:
        messages.error(request, "Kan inte ansluta till kobra.")
    except LiuGetterError:
        messages.error(request, "Fel i anslutingen till kobra.")
    return render(request, "user_managements/kobra.html")