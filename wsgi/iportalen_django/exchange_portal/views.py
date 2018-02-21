from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.utils.translation import ugettext as _
from .models import Exchange_Course, Liu_Course, School, Continent, Country, City, Travel_Story
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

    asia_list = Country.objects.filter(in_continent__name='Asien')
    europa_list = Country.objects.filter(in_continent__name='Europa')
    northamerica_list = Country.objects.filter(in_continent__name='Nordamerika')
    southamerica_list = Country.objects.filter(in_continent__name='Sydamerika')
    africa_list = Country.objects.filter(in_continent__name='Afrika')
    oceania_list = Country.objects.filter(in_continent__name='Oceanien')

    return render(request, 'exchange_portal/exchange_portal.html', {'school_list': school_list, 'asia_list': asia_list, 'europa_list': europa_list, 'northamerica_list': northamerica_list, 'southamerica_list': southamerica_list, 'africa_list': africa_list, 'oceania_list': oceania_list})

def Important_Dates(request):
    return render(request, 'exchange_portal/important_dates.html')


def Contact(request):
    return render(request, 'exchange_portal/contact.html')


def Exchange_School(request, pk):
    course_list = Exchange_Course.objects.filter(in_school=pk)
    school = get_object_or_404(School, pk=pk)
    travel_story = school.travel_story_set.all()
    return render(request, 'exchange_portal/exchange_school.html', {'school': school, 'course_list': course_list, 'travel_story': travel_story})


def Add_Country(request):
    continent_list = Continent.objects.all()
    country_name = request.POST.get('country_name')
    in_continent = request.POST.get('in_continent')
    if country_name != None:
        new_country = Country(name=country_name, in_continent=Continent.objects.get(id=in_continent))
        new_country.save()

    return render(request, 'exchange_portal/add_country.html', {'continent_list': continent_list})


def Add_City(request):
    country_list = Country.objects.all()
    city_name = request.POST.get('city_name')
    country_id = request.POST.get('country_id')
    if city_name != None and country_id!=None:
        new_city = City(name=city_name, in_country=Country.objects.get(id=country_id))
        new_city.save()
    return render(request, 'exchange_portal/add_city.html', {'country_list': country_list})


def Add_School(request):
    country_list = Country.objects.all()
    city_list = City.objects.all() #Lägg till så man väljer land först så man inte behöver gå igenom alla städer som finns
    school_name = request.POST.get('school_name')
    city_id = request.POST.get('city_id')
    freemover = request.POST.get('freemover')
    exchange_with_liu = request.POST.get('exchange_with_liu')
    if freemover == None:
        freemover = False

    if exchange_with_liu == None:
        exchange_with_liu = False

    if school_name != None:
        new_school = School(name=school_name, in_city=City.objects.get(id=city_id), freemover=freemover, exchange_with_liu=exchange_with_liu)
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

def single_travel_story(request, pk):
    travel_story = get_object_or_404(Travel_Story, pk=pk)
    return render(request, 'exchange_portal/travel_story.html', {'travel_story': travel_story})
    #Add all travel stories to show


# Add continents here. If statements is due to limiting the threat of SQL-injection.
def continent(request, continent):
    continent = continent.lower()

    if continent == 'asia':
        countries = Country.objects.filter(in_continent__name='asien')
        return render(request, 'exchange_portal/continent.html', {'continent': 'asien', 'country_list': countries})

    elif continent == 'europe':
        countries = Country.objects.filter(in_continent__name='europa')
        return render(request, 'exchange_portal/continent.html', {'continent': 'europa', 'country_list': countries})

    elif continent == 'africa':
        countries = Country.objects.filter(in_continent__name='afrika')
        return render(request, 'exchange_portal/continent.html', {'continent': 'afrika', 'country_list': countries})


def continent_filtered(request, continent, country):
    country = country.lower()
    #countries = Country.objects.filter(in_continent__name='asien')
    #filtered_country = Country.objects.filter(in_country__name=country)

    return render(request, 'exchange_portal/continent.html', {'country': country})

@login_required()
def Admin(request):
    return render(request, 'exchange_portal/admin.html')
