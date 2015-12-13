from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', view=views.evaluate_course, name="evaluate course"),
    url(r'^admin/$', view=views.admin, name="admin"),
    url(r'^admin/year/$', view=views.choose_year, name="choose year"),
    url(r'^admin/year/create/$', view=views.create_year, name="create year"),
    url(r'^admin/year/(?P<year>[0-9]+)/$', view=views.admin_year, name="admin year"),
    url(r'^admin/period/(?P<pk>[0-9]+)/$', view=views.admin_period, name="admin period"),
    url(r'^admin/period/(?P<pk>[0-9]+)/edit$', view=views.edit_period, name="edit period"),
    url(r'^admin/courses/$', view=views.create_courses, name="create courses"),
    #url(r'^admin/courses/edit$', view=views.create_or_modify_courses, name="edit course"),

    ]