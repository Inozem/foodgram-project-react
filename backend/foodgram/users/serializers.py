from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import User


class CustomUserSerializer(UserSerializer):
    """Класс регистрации и работы с пользователями"""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            password=make_password(validated_data['password']),
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.save()
        return user

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Нельзя создать пользователя me')
        return value


class ChangePasswordSerializer(UserSerializer):
    """Класс изменения пароля у пользователя"""
    current_password = serializers.CharField(source='password', required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password')

    def validate_new_password(self, value):
        return make_password(value)
