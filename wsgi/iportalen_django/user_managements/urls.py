from django.conf.urls import url
from django.contrib.auth.views import password_change, password_change_done
from .views import (
    logout_view,
    login,
    my_page_view,
    change_user_info_view,
    add_users_to_white_list,
    reset_confirm,
    reset_done,
    reset,
    reset_complete,
    update_user_from_kobra,
    become_member,
    update_all_users_from_kobra,
    update_list_of_users_from_kobra,
    admin_menu,
)

urlpatterns = [
    url(r'^logout$', logout_view, name='logout_view'),
    url(r'^login$', login, name='login_view'),
    url(r'^$', my_page_view, name='my page'),
    url(r'^my_page$', my_page_view, name='my page'),
    url(r'^change_user_info$', change_user_info_view, name='change user info view'),
    url(r'^add_users_to_whitelist$', view=add_users_to_white_list, name='add users to whitelist'),
    url(r'^become_member$', view=become_member, name="become member"),
    url(r'^kobra/(?P<liu_id>[a-z]{4,5}\d{3})/$', view=update_user_from_kobra, name="update user from kobra"),
    url(r'^update_all_users_from_kobra/$', view=update_all_users_from_kobra, name="update all users from kobra"),
    url(r'^update_list_of_users_from_kobra/$', view=update_list_of_users_from_kobra,
        name="update list of users from kobra"),

    url(r'^reset/(?P<liu_id>[a-z]{4,5}\d{3})/$', view=reset, name='password_reset'),
    # 1:a starta genom att ange liu-mail
    url(r'^reset/$', view=reset, name='password_reset'),  # 1:a starta genom att ange liu-mail
    url(r'^reset/done/$', view=reset_done, name='password_reset_done'),  # 2:a Visar text om att ett mail skickats
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', view=reset_confirm,
        name='password_reset_confirm'),  # 3:e skapa nytt lösenord
    url(r'^reset/complete/$', view=reset_complete, name='password_reset_complete'),  # 4:e lösenord ändrat och klart


    url(r'^password_change/$', password_change, {"template_name": 'user_managements/change_pw.html'},
        name="password_change"),
    url(r'^password_change/done$', password_change_done, {"template_name":'user_managements/change_pw_done.html'},
        name="password_change_done"),
    url(r'^admin', admin_menu, name='user content'),
]
