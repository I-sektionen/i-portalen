from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.utils.translation import ugettext as _
from .models import Exchange_Course, Liu_Course, School, Country
from django.forms import modelformset_factory
import mimetypes

# Create your views here.
def Exchange_Portal(request):
    country_list = Country.objects.all()
    return render(request, 'exchange_portal/exchange_portal.html', {'country_list': country_list})