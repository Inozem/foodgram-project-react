from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from recipes.models import Ingredient, Ingredients_amount, Recipe, Tag
from users.serializers import UserActionGetSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Класс ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsAmountSerializer(serializers.ModelSerializer):
    """Класс количества ингредиентов."""
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = Ingredients_amount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, value):
        name = value.ingredient.name
        return name

    def get_measurement_unit(self, value):
        measurement_unit = value.ingredient.measurement_unit
        return measurement_unit


class IngredientsAmountCreateRecipeSerializer(serializers.ModelSerializer):
    """Класс количества ингредиентов для создания рецептов."""
    class Meta:
        model = Ingredients_amount
        fields = ('ingredient', 'amount')

    def validate_amount(self, value):
        if value > 0:
            return value
        raise serializers.ValidationError('Количество должно быть больше 0')


class TagSerializer(serializers.ModelSerializer):
    """Класс тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Класс рецептов."""
    author = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    ingredients = IngredientsAmountSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'text',
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
        fields = ('ingredients', 'tags', 'name', 'text', 'cooking_time',
                  'author')

    def to_representation(self, instance):
        request = self.context.get('request')
        print(instance)
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data
