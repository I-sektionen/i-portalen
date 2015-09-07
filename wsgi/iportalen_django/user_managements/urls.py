from django.conf.urls import url, patterns

from .views import logout_view

urlpatterns = patterns('',
    url(r'^logout$', logout_view, name='logout_view'),
    url(r'login', 'django.contrib.auth.views.login', {'template_name': 'user_managments/login.html'}, name='login_view')
   )