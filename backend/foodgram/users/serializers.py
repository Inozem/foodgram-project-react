from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Класс получения токена (авторизация)"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']
        self.fields['email'] = serializers.EmailField()

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['password'] = user.password
        token['email'] = user.email
        return {'token': str(token.access_token)}

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = get_object_or_404(
            User,
            email=email,
        )
        if user.check_password(password):
            return self.get_token(user)
        return 'Неверный пароль'

