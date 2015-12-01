from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .forms import ChangeUserInfoForm, AddWhiteListForm, MembershipForm
from .models import IUser
from django.core.urlresolvers import reverse
from django.contrib import messages
from utils.text import random_string_generator
from django.contrib.auth.views import (
    password_reset_confirm,
    password_reset,
)
from utils.kobra import get_user_by_liu_id, LiuGetterError, LiuNotFoundError
import re
import time


def logout_view(request):
    logout(request)
    return redirect('/')  # TODO: Where should this redirect?


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username.lower(), password=password)

        #  User failed to login, why?
        if user is None:
            #  The user tried an island-id. (format: i12firla)
            if re.match(r"^i\w{2}[a-z]{4}", username):
                messages.error(request, "Använd ditt LiU-id för att logga in, inte Islands-id.")
                return render(request, "user_managements/login.html")

            user_account = IUser.objects.filter(username__exact=username)
            if user_account.exists() and user_account[0].last_login is None and user_account[0].is_active:
                #  The user-account exists, but the user must login in a first time.
                messages.info(request, "Du måste aktivera ditt konto innan du kan logga in första gången.")
                return redirect("password_reset", liu_id=username)
            else:
                # the authentication system was unable to verify the username and password
                messages.error(request, "Fel Liu-id eller lösenord.")
            return render(request, "user_managements/login.html")

        # The user has the right password.
        else:
            if user.is_active:
                if user.is_member is None:
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
                    form = MembershipForm(initial={"user": user.username})
                    return render(request, "user_managements/membership.html", {"form": form})
                elif user.is_member is True:
                    auth_login(request, user)
                    try:
                        return redirect(request.GET['next'])
                    except:
                        return redirect('/')

        # The password is valid, but the account has been disabled! (Användaren Klickade ev: "vill INTE bli medlem")
        messages.error(request, "Lösenordet är korrekt, men kontot är avstängt! "
                                "Om detta inte bör vara fallet var god kontakta info@isektionen.se")
        return render(request, "user_managements/login.html")
    else:
        # Did not try to login.
        return render(request, "user_managements/login.html")


def become_member(request):
    if request.method == 'POST' and 'member' in request.POST:
        form = MembershipForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user'].lower(), password=form.cleaned_data['password'])
            if user is None:
                messages.error(request, "Fel Liu-id eller lösenord.")
                return render(request, "user_managements/membership.html", {"form": form})
            user.is_member = True
            user.save()
            auth_login(request, user)
            messages.info(request,
                          "Tack för att du vill vara medlem i sektionen. Du kan nu utnyttja sektionens tjänster.")
            return redirect("/")
        else:
            messages.error(request, "Fel Liu-id eller lösenord.")
            return render(request, "user_managements/membership.html", {"form": form})

    elif request.method == 'POST' and 'not_member' in request.POST:
        form = MembershipForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user'].lower(), password=form.cleaned_data['password'])
            if user is None:
                messages.error(request, "Fel Liu-id eller lösenord.")
                return render(request, "user_managements/membership.html", {"form": form})
            user.is_member = False
            user.save()
            messages.info(request, "Vad tråkigt att du inte vill vara medlem i sektionen. "
                                   "Om du ångrar dig kan du kontakta Info@isektionen.se")
            return redirect("/")
        else:
            messages.error(request, "Fel Liu-id eller lösenord.")
            return render(request, "user_managements/membership.html", {"form": form})
    else:
        return redirect(reverse("login_view"))


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
        return render(request, "user_managements/user_info_form.html", {'form': form})


@login_required()
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
                temp_user = IUser(username=liu_id.lower(), email=liu_id.lower() + "@student.liu.se")
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
                try:
                    user = IUser.objects.get(username=liu_id)
                    kobra_dict = get_user_by_liu_id(liu_id)
                    user.email = kobra_dict['email'].lower()
                    user.last_name = kobra_dict['last_name'].lower()
                    user.first_name = kobra_dict['first_name'].lower()

                    while len(kobra_dict['rfid_number']) < 10:
                        kobra_dict['rfid_number'] = "0" + kobra_dict['rfid_number']

                    user.rfid_number = kobra_dict['rfid_number']
                    user.p_nr = kobra_dict['personal_number']
                    user.save()
                except IUser.DoesNotExist:
                    messages.error(request, "Användaren {:} sparades inte som den skulle.".format(liu_id))
                except LiuNotFoundError:
                    messages.error(request, "Kan inte ansluta till kobra.")
                except LiuGetterError:
                    messages.error(request, "Fel i anslutingen till kobra.")
            if errors:
                messages.info(request, "De användare utan fel har skapats och kan nu återställa sitt lösenord.")
            else:
                messages.success(request, "De nya användarna har skapats och kan nu återställa sitt lösenord")
    else:
        form = AddWhiteListForm()
    return render(request, "user_managements/add_whitelist.html", {'form': form})


def reset(request, liu_id=None):
    return password_reset(request, template_name='user_managements/reset/pw_res.html',
                          email_template_name='user_managements/reset/pw_res_email.html',
                          subject_template_name='user_managements/reset/pw_res_email_subject.txt',
                          extra_context={'liu_id': liu_id}, )


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='user_managements/reset/pw_res_confirm.html',
                                  uidb64=uidb64,
                                  token=token,
                                  post_reset_redirect=reverse('password_reset_complete'))


def reset_done(request):
    # return password_reset_done(request, template_name='user_managements/reset/pw_res_done.html')
    messages.info(request, "Ett mail kommer inom kort skickas till mailadressen som angavs. "
                           "I den finns en länk för att skapa ett nytt lösenord. "
                           "Om det inte kommer något mail, vänligen kontakta info@isektionen.se")
    return redirect("/")


def reset_complete(request):
    messages.info(request, "Ditt lösenord är uppdaterat, logga in nedan.")
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

        while len(kobra_dict['rfid_number']) < 10:
            kobra_dict['rfid_number'] = "0" + kobra_dict['rfid_number']

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


@login_required()
def update_all_users_from_kobra(request):
    if not request.user.has_perm("user_managements.add_iuser"):
        messages.error(request, "Du har inte rätt behörighet att updatera från kobra.")
        return render(request, "user_managements/kobra.html")
    errors = ""
    users = IUser.objects.all()
    timeout = 0
    for user in users:
        timeout += 1
        if timeout == 10:
            time.sleep(1)
            timeout = 0
        try:

            kobra_dict = get_user_by_liu_id(user.username)
            user.email = kobra_dict['email'].lower()
            user.last_name = kobra_dict['last_name'].lower()
            user.first_name = kobra_dict['first_name'].lower()

            while len(kobra_dict['rfid_number']) < 10:
                kobra_dict['rfid_number'] = "0" + kobra_dict['rfid_number']

            user.rfid_number = kobra_dict['rfid_number']
            user.p_nr = kobra_dict['personal_number']
            user.save()
        except ValueError:
            errors += (user.username + " gick inte att hämta hos kobra.\n")
        except IUser.DoesNotExist:
            errors += (user.username + " finns inte i systemet.\n")
        except LiuNotFoundError:
            errors += (user.username + " kan inte ansluta till kobra.\n")
        except LiuGetterError:
            errors += (user.username + " fel i anslutingen till kobra.\n")
    print(errors)
    return render(request, "user_managements/kobra.html")


@login_required()
def update_list_of_users_from_kobra(request):
    if not request.user.has_perm("user_managements.add_iuser"):
        messages.error(request, "Du har inte rätt behörighet att updatera från kobra.")
        return render(request, "user_managements/kobra.html")
    if request.method == 'POST':
        form = AddWhiteListForm(request.POST)
        if form.is_valid():
            list_of_liu_id = form.cleaned_data['users'].splitlines()
            timeout = 0
            for liu_id in list_of_liu_id:
                timeout += 1
                if timeout == 10:
                    time.sleep(1)
                    timeout = 0
                try:
                    user = IUser.objects.get(username=liu_id)
                    kobra_dict = get_user_by_liu_id(user.username)
                    user.email = kobra_dict['email'].lower()
                    user.last_name = kobra_dict['last_name'].lower()
                    user.first_name = kobra_dict['first_name'].lower()

                    while len(kobra_dict['rfid_number']) < 10:
                        kobra_dict['rfid_number'] = "0" + kobra_dict['rfid_number']

                    user.rfid_number = kobra_dict['rfid_number']
                    user.p_nr = kobra_dict['personal_number']
                    user.save()
                except ValueError:
                    messages.error(request, liu_id + " gick inte att hämta hos kobra.\n")
                except IUser.DoesNotExist:
                    messages.error(request, liu_id + " finns inte i systemet.\n")
                except LiuNotFoundError:
                    messages.error(request, liu_id + " kan inte ansluta till kobra.\n")
                except LiuGetterError:
                    messages.error(request, liu_id + " fel i anslutingen till kobra.\n")
    else:
        form = AddWhiteListForm()
    return render(request, "user_managements/add_whitelist.html", {'form': form})
