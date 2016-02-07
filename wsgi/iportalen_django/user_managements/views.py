from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ChangeUserInfoForm, AddWhiteListForm, MembershipForm, MembershipForm, SegmentUsersForm, SelectUserFieldsForm
from .models import IUser, IpikureSubscriber
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from utils.text import random_string_generator
from django.contrib.auth.views import (
    password_reset_confirm,
    password_reset,
)
from utils.kobra import get_user_by_liu_id, LiuGetterError, LiuNotFoundError
import re
import time
import operator


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
                messages.error(request, "Fel Liu-id eller lösenord. Om felet kvarstår kontakta medlem@i-portalen.se ")
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
                    if user.must_edit:
                        form = ChangeUserInfoForm(instance=user)
                        return render(request, "user_managements/force_user_form.html", {"form": form})
                    auth_login(request, user)
                    try:
                        return redirect(request.GET['next'])
                    except:
                        return redirect('/')

        # The password is valid, but the account has been disabled! (Användaren Klickade ev: "vill INTE bli medlem")
        messages.error(request, "Lösenordet är korrekt, men kontot är avstängt! "
                                "Om detta inte bör vara fallet var god kontakta medlem@i-portalen.se")
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
            messages.info(request,
                          "Tack för att du vill vara medlem i sektionen.")
            if user.must_edit:
                form = ChangeUserInfoForm(instance=user)
                return render(request, "user_managements/force_user_form.html", {"form": form})
            auth_login(request, user)

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
                                   "Om du ångrar dig kan du kontakta info@isektionen.se")
            return redirect("/")
        else:
            messages.error(request, "Fel Liu-id eller lösenord.")
            return render(request, "user_managements/membership.html", {"form": form})
    else:
        return redirect(reverse("login_view"))


def force_change_user_info_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username.lower(), password=password)
        if user is None:
            messages.error(request, "Fel Liu-id eller lösenord.")
            form = ChangeUserInfoForm(request.POST)
            return render(request, "user_managements/force_user_form.html", {"form": form})
        form = ChangeUserInfoForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            user.must_edit = False
            user.save()
            auth_login(request, user)
            messages.info(request,
                          "Tack! Nu kan du utnyttja sektionens tjänster.")
            return redirect("/")
        else:
            messages.error(request, "Fel Liu-id eller lösenord.")
            return render(request, "user_managements/force_user_form.html", {"form": form})
    else:
        return redirect(reverse("login_view"))


@login_required()
def my_page_view(request):
    user = request.user
    if request.method == 'POST':
        change_user_info_form = ChangeUserInfoForm(request.POST, instance=user)
        if change_user_info_form.is_valid():
            change_user_info_form.save()
        return render(request, "user_managements/user-profile.html",
                      {'form': change_user_info_form, 'tab2': "is-active"})
    else:
        change_user_info_form = ChangeUserInfoForm(instance=user)
        return render(request, "user_managements/user-profile.html",
                      {'form': change_user_info_form, 'tab1': "is-active"})


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

@login_required()
def subscribe_to_ipikure(request):
    # return password_reset_done(request, template_name='user_managements/reset/pw_res_done.html')
    if not (request.user.address and request.user.zip_code and request.user.city):
        messages.error(request, "Du måste ange din adress för att kunna prenumerera på ipikuré")
        return redirect(reverse("my page"))
    try:
        subscriber = IpikureSubscriber.objects.get(user=request.user)
        subscriber.date_subscribed = timezone.now()
        subscriber.save()
        messages.info(request, "Du har nu uppdaterat din prenumeration av Ipikuré")
    except IpikureSubscriber.DoesNotExist:
        IpikureSubscriber.objects.create(user=request.user)
        messages.info(request, "Du prenumererar nu på Ipikuré")
    return redirect(reverse("my page"))

@login_required()
def ipikure_subscribers(request):
    subscribers = IpikureSubscriber.objects.all().order_by('user__username')

    return render(request, "user_managements/ipikure_subscribers.html",
                          {'subscribers_list': subscribers})
@login_required()
def admin_menu(request):
    return render(request, "user_managements/user_admin.html")

@login_required()
@permission_required('user_managements.can_view_users')
def filter_users(request):
    users = None
    select_user_fields_form = SelectUserFieldsForm()
    if request.method == 'POST':
        form = SegmentUsersForm(request.POST)
        if form.is_valid():
            query = Q()
            # Gender:
            gender = form.cleaned_data['gender']
            if gender:
                queries = [Q(gender=x) for x in gender]
                temp_query = queries.pop()
                for item in queries:
                    temp_query |= item
                query &= temp_query

            # Start year:
            start_year = form.cleaned_data['start_year']
            if start_year:
                query &= Q(start_year__exact=start_year)

            # Bachelor:
            bachelor_profile = form.cleaned_data['bachelor_profile']
            if bachelor_profile:
                queries = [Q(bachelor_profile=x) for x in bachelor_profile]
                temp_query = queries.pop()
                for item in queries:
                    temp_query |= item
                query &= temp_query

            # Master:
            master_profile = form.cleaned_data['master_profile']
            if master_profile:
                queries = [Q(master_profile=x) for x in master_profile]
                temp_query = queries.pop()
                for item in queries:
                    temp_query |= item
                query &= temp_query

            # current year:
            current_year = form.cleaned_data['current_year']
            if current_year:
                queries = [Q(current_year=x) for x in current_year]
                temp_query = queries.pop()
                for item in queries:
                    temp_query |= item
                query &= temp_query

            # class letter:
            klass = form.cleaned_data['klass']
            if klass:
                queries = [Q(klass=x) for x in klass]
                temp_query = queries.pop()
                for item in queries:
                    temp_query |= item
                query &= temp_query

            #  Only active members:
            query &= Q(is_active=True)

            #  Final database query:
            users = IUser.objects.filter(query)  # Search result
        else:
            users = None  # Not valid form
    else:
        form = SegmentUsersForm()  # First time

    return render(request, 'user_managements/search_users.html', {
        'form': form,
        'users': users,
        'select_user_fields_form': select_user_fields_form,
    })


@login_required()
@permission_required('user_managements.can_view_users')
def all_users(request):
    users = IUser.objects.all()
    return render(request, 'user_managements/all_users.html', {
        'users': users,
    })


@login_required()
def profile_page(request, liu_id):
    u = get_object_or_404(IUser, username=liu_id)
    return render(request, 'user_managements/profile_page.html',{
        'user': u,
    })
