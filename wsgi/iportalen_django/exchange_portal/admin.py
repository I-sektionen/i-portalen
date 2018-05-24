from django.contrib import admin
from .models import Continent, Country, School, Liu_Course, Exchange_Course, Travel_Story, City, Feedback
from utils.admin import HiddenModelAdmin, iportalen_admin_site, iportalen_superadmin_site

iportalen_admin_site.register(Continent)
iportalen_admin_site.register(Country)
iportalen_admin_site.register(School)
iportalen_admin_site.register(City)
iportalen_admin_site.register(Liu_Course)
iportalen_admin_site.register(Exchange_Course)
iportalen_admin_site.register(Travel_Story)
iportalen_admin_site.register(Feedback)

iportalen_superadmin_site.register(Continent)
iportalen_superadmin_site.register(Country)
iportalen_superadmin_site.register(School)
iportalen_superadmin_site.register(City)
iportalen_superadmin_site.register(Liu_Course)
iportalen_superadmin_site.register(Exchange_Course)
iportalen_superadmin_site.register(Travel_Story)
iportalen_superadmin_site.register(Feedback)
