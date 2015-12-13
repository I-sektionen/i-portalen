from django.contrib import admin
from .models import Course, Reward, Evaluation, Period, Year

admin.site.register(Year)
admin.site.register(Course)
admin.site.register(Reward)
admin.site.register(Evaluation)
admin.site.register(Period)
