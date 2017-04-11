from django.shortcuts import render


def landing(request):
    return render(request, "webgroup/landing.html", {})


def github_stats(request):
    return render(request, "webgroup/github.html", {})
