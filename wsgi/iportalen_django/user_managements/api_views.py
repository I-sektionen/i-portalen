# ViewSets define the view behavior.
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import IUser, BachelorProfile, MasterProfile
from .serializers import IUserSerializer, BachelorProfileSerializer, MasterProfileSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class IUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IUser.objects.all()
    serializer_class = IUserSerializer
    lookup_field = 'username'
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = StandardResultsSetPagination
    filter_fields = ('username',
                     'id',
                     "gender",
                     "allergies",
                     "start_year",
                     "current_year",
                     "klass",
                     "bachelor_profile",
                     "master_profile",
                     "rfid_number",
                     "is_member"
                     )


class BachelorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BachelorProfile.objects.all()
    serializer_class = BachelorProfileSerializer


class MasterProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MasterProfile.objects.all()
    serializer_class = MasterProfileSerializer