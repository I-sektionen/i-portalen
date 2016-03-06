from django.shortcuts import render
from .models import School, Exchange_Course
# Create your views here.

def show_utlandsportalen(request):
    return render(request, "utlandsportalen/utlandsportalen.html")

def show_schools(request):
    schools = School.objects.all
    courses = Exchange_Course.objects.all
    return render(request, "utlandsportalen/schools.html", {'schools': schools, 'courses': courses})

def show_blogs(request):
    return render(request, "utlandsportalen/blogs.html")

def show_contact(request):
    return render(request, "utlandsportalen/contact.html")

def show_scholarships(request):
    return render(request, "utlandsportalen/scholarships.html")