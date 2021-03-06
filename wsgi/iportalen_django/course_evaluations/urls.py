from django.conf.urls import url, include
from . import views

app_name = 'course_evaluations'

course_evaluations_patterns = [
    url(r'^$',                                         view=views.evaluate_course,          name="evaluate course"),
    url(r'^admin/$',                                   view=views.admin,                    name="admin"),
    url(r'^admin/year/$',                              view=views.choose_year,              name="choose year"),
    url(r'^admin/year/copy/$',                         view=views.copy_last_year,           name="copy year"),
    url(r'^admin/year/create/$',                       view=views.create_year,              name="create year"),
    url(r'^admin/year/(?P<year>[0-9]+)/$',             view=views.admin_year,               name="admin year"),
    url(r'^admin/period/(?P<pk>[0-9]+)/$',             view=views.admin_period,             name="admin period"),
    url(r'^admin/period/(?P<pk>[0-9]+)/edit$',         view=views.edit_period,              name="edit period"),
    url(r'^admin/period/(?P<pk>[0-9]+)/evaluations/$', view=views.evaluations,              name="evaluations"),
    url(r'^admin/courses/$',                           view=views.create_courses,           name="create courses"),
    url(r'^admin/rewards/$',                           view=views.create_or_modify_rewards, name="edit rewards"),
]

urlpatterns = [url(r'^', include(course_evaluations_patterns, namespace=app_name))]
