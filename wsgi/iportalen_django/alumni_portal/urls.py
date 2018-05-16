from django.conf.urls import url, include
from . import views

app_name = 'alumni_portal'


alumni_patterns = [
    url(r'^$', view=views.alumni_portal, name='alumni_portal'),
    url(r'^alumni_magazine/$', view=views.alumni_magazine, name="alumni_magazine"),
    url(r'^alumni_article/(?P<pk>[0-9]+)/$', view=views.single_article, name='alumni_article'),
    url(r'^skugga_en_alumn/$', view=views.alumni_skugga, name="skugga_en_alumn"),
    url(r'^about/$', view=views.about, name="about"),
    url(r'^mentorship_program/$', view=views.mentorship_program, name="mentorship_program"),
    url(r'^calendar/$', view=views.calendar, name="calendar"),
]

urlpatterns = [url(r'^', include(alumni_patterns, namespace=app_name))]
