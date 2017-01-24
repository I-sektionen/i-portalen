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

# Create your views here.
def Exchange_Portal(request):
    country_list = Country.objects.all()
    return render(request, 'exchange_portal/exchange_portal.html', {'country_list': country_list})

def Search (request):
    query = request.POST.get('q')
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

'''def single_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.can_administer(request.user):
        admin = True
    else:
        admin = False
    if (article.status == Article.APPROVED and article.show_article_before_experation) or admin:
        attachments = article.otherattachment_set
        image_attachments = article.imageattachment_set
        return render(request, 'articles/article.html', {
            'article': article,
            'attachments': attachments,
            'image_attachments': image_attachments,
            'can_administer': admin})
    raise PermissionDenied'''