from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$', view=views.evaluate_course, name="evaluate_course"),
    ]