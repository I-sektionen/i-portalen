from django.contrib import admin
from .models import Course, Reward, Evaluation, Period, Year, CourseEvaluationSettings
from utils.admin import HiddenModelAdmin
from utils.admin import iportalen_admin_site

iportalen_admin_site.register(Year, HiddenModelAdmin)
iportalen_admin_site.register(Course, HiddenModelAdmin)
iportalen_admin_site.register(Reward, HiddenModelAdmin)
iportalen_admin_site.register(Evaluation, HiddenModelAdmin)
iportalen_admin_site.register(Period, HiddenModelAdmin)
iportalen_admin_site.register(CourseEvaluationSettings)
