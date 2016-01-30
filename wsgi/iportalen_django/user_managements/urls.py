from django.conf.urls import url, include
from django.contrib.auth.views import password_change, password_change_done
from . import views

app_name = 'user_management'

default_django_patterns = [
    # 1:a starta genom att ange liu-mail
    url(r'^reset/(?P<liu_id>[a-z]{4,5}\d{3})/$', view=views.reset, name='password_reset'),
    url(r'^reset/$', view=views.reset, name='password_reset'),

    # 2:a Visar text om att ett mail skickats
    url(r'^reset/done/$', view=views.reset_done, name='password_reset_done'),

    # 3:e skapa nytt lösenord
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', view=views.reset_confirm,
        name='password_reset_confirm'),

    # 4:e lösenord ändrat och klart
    url(r'^reset/complete/$', view=views.reset_complete, name='password_reset_complete'),

    url(r'^password_change/$', password_change, {"template_name": 'user_managements/change_pw.html'},
        name="password_change"),
    url(r'^password_change/done$', password_change_done, {"template_name": 'user_managements/change_pw_done.html'},
        name="password_change_done"),

    url(r'^logout$', view=views.logout_view, name='logout_view'),
    url(r'^login$', view=views.login, name='login_view'),
]

user_patterns = [
    url(r'^$', view=views.my_page_view, name='my page'),
    url(r'^(?P<liu_id>[a-z]{4,5}\d{3})/$', view=views.profile_page, name="profile page"),
    url(r'^add_users_to_whitelist$', view=views.add_users_to_white_list, name='add users to whitelist'),
    url(r'^become_member$', view=views.become_member, name="become member"),
    url(r'^force_user_info', view=views.force_change_user_info_view, name="force user info"),
    url(r'^kobra/(?P<liu_id>[a-z]{4,5}\d{3})/$', view=views.update_user_from_kobra, name="update user from kobra"),
    url(r'^update_all_users_from_kobra/$', view=views.update_all_users_from_kobra, name="update all users from kobra"),
    url(r'^update_list_of_users_from_kobra/$', view=views.update_list_of_users_from_kobra,
        name="update list of users from kobra"),

    url(r'^admin$', views.admin_menu, name="user content"),
    url(r'^subscribe_to_ipikure$', view=views.subscribe_to_ipikure, name="subscribe to ipikure"),
    url(r'^ipikure_subscribers$', view=views.ipikure_subscribers, name="ipikure subscribers"),
    url(r'^search_users/', view=views.filter_users, name="filter users"),
    url(r'^all_users/', view=views.all_users, name="all users"),
]

urlpatterns = [
    url(r'^', include(user_patterns, namespace=app_name)),
    url(r'^', include(default_django_patterns))
]