from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from recipes.models import Recipe
from users.serializers import UserActionGetSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """Класс регистрации пользователей"""
    author = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text',
                  'cooking_time')

    def get_author(self, value):
        serializer = UserActionGetSerializer(self.context['request'].user)
        return serializer.data
