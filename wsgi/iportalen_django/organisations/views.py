from django.shortcuts import render
from .models import Organisation

# Create your views here.
def all_organisations(request):
    return render(request, "organisations/organisations.html", {'organisations': Organisation.objects.all()})

def organisation(request, organisation_name):
    return render(request, "organisations/organisation.html", {'organisation': Organisation.objects.get(name=organisation_name)})

def edit_organisation(request, organisation_name):
    # Edit org.
    return render(request, "organisations/organisation.html", {'organisation': Organisation.objects.get(name=organisation_name)})