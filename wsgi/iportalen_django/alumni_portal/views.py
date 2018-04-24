from django.shortcuts import render
from .models import Alumni_Article, Magazine


def alumni_portal(request):
    articles = Alumni_Article.objects.published()
    return render(request, 'alumni_portal.html', {'articles': articles})


def alumni_magazine(request):
    magazines = Magazine.objects.order_by('-date')
    return render(request, 'alumni_magazine.html', {'magazines': magazines})
