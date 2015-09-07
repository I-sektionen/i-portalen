from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


def logout_view(request):
    logout(request)
    return redirect('/')  # TODO: Where should this redirect?