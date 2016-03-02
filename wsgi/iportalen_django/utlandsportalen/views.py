
from django.shortcuts import render

# Create your views here.

def show_utlandsportalen(request):
    return render(request, "utlandsportalen/utlandsportalen.html")

def show_blogs(request):
    return render(request, "utlandsportalen/blogs.html")

def show_contact(request):
    return render(request, "utlandsportalen/contact.html")

def show_scholarships(request):
    return render(request, "utlandsportalen/scholarships.html")