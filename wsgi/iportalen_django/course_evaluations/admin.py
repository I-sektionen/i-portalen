from .models import Course, Reward, Evaluation, Period, Year, CourseEvaluationSettings
from utils.admin import HiddenModelAdmin
from utils.admin import iportalen_admin_site
from django.contrib import admin


iportalen_admin_site.register(Year, HiddenModelAdmin)
iportalen_admin_site.register(Course, HiddenModelAdmin)
iportalen_admin_site.register(Reward, HiddenModelAdmin)
iportalen_admin_site.register(Evaluation, HiddenModelAdmin)
iportalen_admin_site.register(Period, HiddenModelAdmin)
iportalen_admin_site.register(CourseEvaluationSettings)

admin.site.register(Year)
admin.site.register(Course)
admin.site.register(Reward)
admin.site.register(Evaluation)
admin.site.register(Period)
admin.site.register(CourseEvaluationSettings)
