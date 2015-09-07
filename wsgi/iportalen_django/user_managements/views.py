from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout


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