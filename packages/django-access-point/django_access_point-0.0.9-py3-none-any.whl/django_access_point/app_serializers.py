from django_access_point.serializers.crud import CrudSerializer
from django_access_point.serializers.custom_field import CustomFieldSerializer

from .models import User, UserCustomField, UserCustomFieldValue


class UserCustomFieldSerializer(CustomFieldSerializer):
    class Meta:
        model = UserCustomField


class UserSerializer(CrudSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "phone_no"]
