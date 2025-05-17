from rest_framework import serializers
from .models import User
import uuid
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError(_('Неверные учетные данные.'))
            
            if not user.is_active:
                raise serializers.ValidationError(_('Аккаунт не активирован. Пожалуйста, подтвердите ваш email.'))
            
            if not user.is_email_confirmed:
                raise serializers.ValidationError(_('Email не подтвержден. Пожалуйста, подтвердите ваш email.'))
        else:
            raise serializers.ValidationError(_('Необходимо указать имя пользователя и пароль.'))

        data['user'] = user
        return data
