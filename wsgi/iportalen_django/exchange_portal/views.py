from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.utils.translation import ugettext as _
from .models import Exchange_Course, Liu_Course, School, Country, City, Travel_Story
from django.forms import modelformset_factory
import mimetypes
from django.db.models import Q
from dal import autocomplete

# Create your views here.
def Exchange_Portal(request):
    query = request.POST.get('q')
    if query != None:
        school_list = School.objects.filter(Q(name__icontains=query) | Q(in_city__name__icontains=query) |
                                        Q(in_city__in_country__name__icontains=query))
    else:
        school_list = None

    asia_list = Country.objects.filter(Q(continent__incontrains='Asien'))
    return render(request, 'exchange_portal/exchange_portal.html', {'school_list': school_list, 'asia_list': asia_list})

def Important_Dates(request):
    return render(request, 'exchange_portal/important_dates.html')


def Contact(request):
    return render(request, 'exchange_portal/contact.html')


def Exchange_School(request, pk):
    school = get_object_or_404(School, pk=pk)
    course_list = Exchange_Course.objects.filter(in_school=pk)

    school = get_object_or_404(School, pk=pk)
    travel_story = school.travel_story_set.all()

    return render(request, 'exchange_portal/exchange_school.html', {'school': school, 'course_list': course_list, 'travel_story': travel_story})


def Add_Country(request):
    query = request.POST.get('q')
    if query != None:
        new_country = Country(name=query)
        new_country.save()

    return render(request, 'exchange_portal/add_country.html')


def Add_City(request):
    country_list = Country.objects.all()
    city_name = request.POST.get('city_name')
    country_id = request.POST.get('country_id')
    if city_name != None:
        new_city = City(name=city_name, in_country=Country.objects.get(id=country_id))
        new_city.save()
    return render(request, 'exchange_portal/add_city.html', {'country_list': country_list})


def Add_School(request):
    city_list = City.objects.all() #Lägg till så man väljer land först så man inte behöver gå igenom alla städer som finns
    school_name = request.POST.get('school_name')
    city_id = request.POST.get('city_id')
    if school_name != None:
        new_school = School(name=school_name, in_city=City.objects.get(id=city_id))
        new_school.save()
    return render(request, 'exchange_portal/add_school.html', {'city_list': city_list})


def Add_Liu_Course(request):
    liu_course_name = request.POST.get('liu_course_name')
    liu_course_code = request.POST.get('liu_course_code') #Borde spara alla i små bokstäver
    is_compulsary = request.POST.get('is_compulsary')
    if is_compulsary == None:
        is_compulsary = False

    if liu_course_code != None and liu_course_name != None:
        new_liu_course = Liu_Course(name=liu_course_name, course_code=liu_course_code, is_compulsary=is_compulsary)
        new_liu_course.save()
    return render(request, 'exchange_portal/add_liu_course.html')


def Add_Exchange_Course(request):
    school_list = School.objects.all()
    liu_course_list = Liu_Course.objects.all()
    exchange_course_name = request.POST.get('exchange_course_name')
    exchange_course_code = request.POST.get('exchange_course_code')
    school_id = request.POST.get('school_id')
    liu_course_id = request.POST.get('liu_course_id')
    if exchange_course_name != None and exchange_course_code != None and school_id != None and liu_course_id != None:
        new_exchange_course = Exchange_Course(name=exchange_course_name,
                                              course_code=exchange_course_code,
                                              in_school=School.objects.get(id=school_id),
                                              corresponding_liu_course=Liu_Course.objects.get(id=liu_course_id),
                                              year=3)
        new_exchange_course.save()
    return render(request, 'exchange_portal/add_exchange_course.html', {'school_list': school_list, 'liu_course_list': liu_course_list})


class Search_Autocomplete (autocomplete.Select2QuerySetView):
    def get_queryset(self):
        #Can have a filter for non authenticades users here if needed

        qs = School.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

def Travel_Stories(request):
    #Search function
    travel_story_list = list(Travel_Story.objects.all())
    #Add all travel stories to show
    return render(request, 'exchange_portal/travel_stories.html', {'travel_story_list':travel_story_list})

def Asia(request):

    return render(request, 'exchange_portal/asia.html')
