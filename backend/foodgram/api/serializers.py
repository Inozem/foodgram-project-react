from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag
from users.serializers import UserActionGetSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Класс тэгов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Класс тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Класс рецептов."""
    author = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text',
                  'cooking_time')

    def get_author(self, value):
        request = self.context['request']
        author = value.author
        context = {'request': request}
        serializer = UserActionGetSerializer(author, context=context)
        return serializer.data

    def validate_cooking_time(self, value):
        if value >= 1:
            return value
        raise serializers.ValidationError('Время готовки должно быть больше 0')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Класс создания рецептов."""
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text',
                  'cooking_time')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data
