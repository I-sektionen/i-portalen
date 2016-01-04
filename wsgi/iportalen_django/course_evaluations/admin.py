from django.contrib import admin
from .models import Course, Reward, Evaluation, Period, Year, CourseEvaluationSettings
from utils.admin import HiddenModelAdmin

admin.site.register(Year, HiddenModelAdmin)
admin.site.register(Course, HiddenModelAdmin)
admin.site.register(Reward, HiddenModelAdmin)
admin.site.register(Evaluation, HiddenModelAdmin)
admin.site.register(Period, HiddenModelAdmin)
admin.site.register(CourseEvaluationSettings)
