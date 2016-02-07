from django.conf.urls import url, include
from . import views

app_name = "bookings"

invoice_patterns = [
    url(r'^create_custom/(?P<booking_pk>[0-9]+)$',
        view=views.create_invoice, name="create custom invoice"),
    url(r'^(?P<invoice_id>[0-9]+)/$',
        view=views.invoice, name="invoice view"),
    url(r'^(?P<invoice_pk>[0-9]+)/email/$',
        view=views.send_invoice_email, name="send invoice email"),
]

booking_patterns = [
    url(r'^$',
        view=views.index, name="my bookings"),
    url(r'^book/(?P<bookable_id>[0-9]+)/$',
        view=views.make_booking, name="make booking"),
    url(r'^book/(?P<bookable_id>[0-9]+)/(?P<weeks_forward>[0-9]+)/$',
        view=views.make_booking, name="make booking week"),
    url(r'^book/(?P<bookable_id>[0-9]+)/api/$',
        view=views.api_view, name="api booking"),
    url(r'^book/(?P<bookable_id>[0-9]+)/api/(?P<weeks_forward>[0-9]+)/$',
        view=views.api_view, name="api booking week_forward"),
    url(r'^(?P<booking_id>[0-9]+)/delete$',
        view=views.remove_booking, name="remove booking"),

    url(r'^invoice/', include(invoice_patterns)),
]

urlpatterns = [url(r'^', include(booking_patterns, namespace=app_name))]
