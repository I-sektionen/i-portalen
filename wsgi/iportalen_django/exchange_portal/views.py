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


# Create your views here.
def Exchange_Portal(request):


    query = request.POST.get('q')
    if query != None:
        school_list = School.objects.filter(Q(name__icontains=query) | Q(in_city__name__icontains=query) |
                                        Q(in_city__in_country__name__icontains=query))
    else:
        school_list = None

    return render(request, 'exchange_portal/exchange_portal.html', {'school_list': school_list})


def Important_Dates(request):
    return render(request, 'exchange_portal/important_dates.html')


def Contact(request):
    return render(request, 'exchange_portal/contact.html')


def Exchange_School(request, pk):
    school = get_object_or_404(School, pk=pk)
    course_list = Exchange_Course.objects.filter(in_school=pk)
    return render(request, 'exchange_portal/exchange_school.html', {'school': school, 'course_list': course_list})

    print(query)
    country_list = Country.objects.filter(name__icontains=query)
    city_list = City.objects.filter(name__icontains=query)
    school_list = School.objects.filter(name__icontains=query)
    return render(request, 'exchange_portal/search_result.html', {'country_list': country_list, 'city_list': city_list,
                                                                  'school_list': school_list})

def View_Story (request, school_pk):

    school = get_object_or_404(School, pk=school_pk)
    travel_story = school.travel_story_set.all()
    #print (travel_story.about_school)
    return render(request, 'exchange_portal/travel_story.html', {'travel_story': travel_story })

