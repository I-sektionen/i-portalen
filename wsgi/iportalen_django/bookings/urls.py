__author__ = 'isac'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'all/', views.index, name="index"),
]
