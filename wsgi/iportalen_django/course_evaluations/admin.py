from .models import Course, Reward, Evaluation, Period, Year, CourseEvaluationSettings
from utils.admin import HiddenModelAdmin
from utils.admin import iportalen_admin_site, iportalen_superadmin_site
from django.contrib import admin


iportalen_admin_site.register(Year, HiddenModelAdmin)
iportalen_admin_site.register(Course, HiddenModelAdmin)
iportalen_admin_site.register(Reward, HiddenModelAdmin)
iportalen_admin_site.register(Evaluation, HiddenModelAdmin)
iportalen_admin_site.register(Period, HiddenModelAdmin)
iportalen_admin_site.register(CourseEvaluationSettings)

iportalen_superadmin_site.register(Year)
iportalen_superadmin_site.register(Course)
iportalen_superadmin_site.register(Reward)
iportalen_superadmin_site.register(Evaluation)
iportalen_superadmin_site.register(Period)
iportalen_superadmin_site.register(CourseEvaluationSettings)
