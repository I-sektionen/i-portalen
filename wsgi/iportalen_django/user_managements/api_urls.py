from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from user_managements import api_views as user_managements_api_views
router = DefaultRouter()
router.register(r'iusers', user_managements_api_views.IUserViewSet)
router.register(r'bachelor_profile', user_managements_api_views.BachelorProfileViewSet)
router.register(r'master_profile', user_managements_api_views.MasterProfileViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
]