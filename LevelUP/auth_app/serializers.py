from rest_framework import serializers
from todo.models import User
from djoser.serializers import UserCreateSerializer

class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password')

class UserSerializer(serializers.ModelSerializer):
    level = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'xp', 'level']