__author__ = 'isac'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^book/(?P<bookable_id>[0-9]+)/$', views.make_booking, name="make_booking"),
    url(r'^book/(?P<bookable_id>[0-9]+)/(?P<year>[0-9]+)/(?P<week>[0-9]+)/$', views.make_booking, name="make_booking"),
    url(r'^invoice/(?P<invoice_id>[0-9]+)', views.invoice_pdf, name="invoice_pdf"),
    url(r'^$', views.index, name="index"),
]
