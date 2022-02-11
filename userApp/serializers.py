from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import Organization

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name', 'is_staff', 'organization']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'is_staff', 'last_name', 'organization']
        ref_name = "User 1"

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Organization
        fields = ('name', 'id')