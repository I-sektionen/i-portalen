from django.conf.urls import url, patterns

from .views import logout_view, login, my_page_view, change_user_info_view

urlpatterns = patterns('',
    url(r'^logout$', logout_view, name='logout_view'),
    # url(r'login', 'django.contrib.auth.views.login', {'template_name': 'user_managments/login.html'}, name='login_view')
    url(r'^login$', login, name='login_view'),
    url(r'^my_page$', my_page_view, name='mypage_view'),
    url(r'^change_user_info$', change_user_info_view, name='change_user_info_view'),

   )
