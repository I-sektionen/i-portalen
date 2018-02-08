from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect




def landing(request):
    return render(request, "webgroup/landing.html", {})


def github_stats(request):
    return render(request, "webgroup/github.html", {})









