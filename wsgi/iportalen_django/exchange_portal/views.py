from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.utils.translation import ugettext as _
from .models import Exchange_Course, Liu_Course, School, Country, City
from django.forms import modelformset_factory
import mimetypes
from django.db.models import Q


# Create your views here.
def Exchange_Portal(request):
    country_list = Country.objects.all()
    return render(request, 'exchange_portal/exchange_portal.html', {'country_list': country_list})


def Search (request):
    query = request.POST.get('q')
    school_list = School.objects.filter(Q(name__icontains=query) | Q(in_city__name__icontains=query) |
                                        Q(in_city__in_country__name__icontains=query))
    return render(request, 'exchange_portal/search_result.html', {'school_list': school_list})


def Exchange_School(request, pk):
    school = get_object_or_404(School, pk=pk)
    course_list = Exchange_Course.objects.filter(in_school=pk)
    return render(request, 'exchange_portal/exchange_school.html', {'school': school, 'course_list': course_list})