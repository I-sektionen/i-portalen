from django.conf.urls import url, patterns

from .views import logout_view, login, my_page_view, change_user_info_view, add_users_to_white_list, set_user_as_member


urlpatterns = patterns('',
    url(r'^logout$', logout_view, name='logout_view'),
    # url(r'login', 'django.contrib.auth.views.login', {'template_name': 'user_managments/login.html'}, name='login_view')
    url(r'^login$', login, name='login_view'),
    url(r'^my_page$', my_page_view, name='mypage_view'),
    url(r'^change_user_info$', change_user_info_view, name='change_user_info_view'),
    url(r'^add_users_to_whitelist$', view=add_users_to_white_list, name='add users to whitelist'),
    url(r'^become_member$', view=set_user_as_member, name="become member")

   )
