from rest_framework import serializers

from user_managements.models import IUser, MasterProfile, BachelorProfile


class IUserSerializer(serializers.ModelSerializer):
    personal_code_number = serializers.SerializerMethodField('get_p_nr')

    class Meta:
        model = IUser
        fields = ('id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'date_joined',
                  'is_active',
                  'is_staff',
                  'is_superuser',
                  'personal_code_number',
                  'address',
                  'zip_code',
                  'city',
                  'gender',
                  'allergies',
                  'start_year',
                  'current_year',
                  'klass',
                  'bachelor_profile',
                  'master_profile',
                  'rfid_number',
                  'is_member',
                  'must_edit',
                  'phone')


class MasterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProfile
        fields = ('id', 'name', 'info', 'link')


class BachelorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BachelorProfile
        fields = ('id', 'name', 'info', 'link')
