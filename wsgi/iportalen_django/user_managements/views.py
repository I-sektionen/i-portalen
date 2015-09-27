from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .forms import ChangeUserInfoForm
from django.core.urlresolvers import reverse


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
                auth_login(request, user)
                try:
                    return redirect(request.GET['next'])
                except:
                    return redirect('/')
            else:
                return render(request, "user_managements/login.html",
                          {'message': "The password is valid, but the account has been disabled!"})
                # The password is valid, but the account has been disabled!
        else:
            # the authentication system was unable to verify the username and password
            return render(request, "user_managements/login.html",
                          {'message': "The username and password were incorrect."})
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