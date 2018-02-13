from django.shortcuts import render
from .models import Alumni_Article



def alumni_portal(request):
    articles = Alumni_Article.objects.published()
    return render(request, 'alumni_portal.html', {'articles': articles})

# def all_articles(request):


