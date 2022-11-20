from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, IngredientsAmount, Recipe,
                            ShoppingCart, Tag)
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
        model = IngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, value):
        name = value.ingredient.name
        return name

    def get_measurement_unit(self, value):
        measurement_unit = value.ingredient.measurement_unit
        return measurement_unit


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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_author(self, value):
        request = self.context['request']
        author = value.author
        context = {'request': request}
        serializer = UserActionGetSerializer(author, context=context)
        return serializer.data

    def favorited_or_in_shopping_cart(self, value, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            object = obj.objects.filter(recipe=value, user=user)
            return object.exists()
        return False  # Если пользователь аноним

    def get_is_favorited(self, value):
        return self.favorited_or_in_shopping_cart(value, obj=Favorite)

    def get_is_in_shopping_cart(self, value):
        return self.favorited_or_in_shopping_cart(value, obj=ShoppingCart)

    def validate_cooking_time(self, value):
        if value >= settings.MIN_COOKING_TIME:
            return value
        raise serializers.ValidationError('Время готовки должно быть больше 0')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Класс создания рецептов."""
    image = Base64ImageField()
    ingredients = serializers.ListField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name', 'text', 'cooking_time',
                  'author', 'image')

    def validate_ingredients(self, value):
        ingredients_id = [ingredient['id'] for ingredient in value]
        if len(ingredients_id) != len(set(ingredients_id)):
            raise serializers.ValidationError(
                'Ингредиенты не должны дублироваться'
            )
        validated_ingredients = []
        for ingredient_value in value:
            min_amount = settings.MIN_INGREDIENTS_AMOUNT
            if int(ingredient_value['amount']) < min_amount:
                raise serializers.ValidationError(
                    'Количество ингредиентов должно быть больше 0'
                )
            ingredient_id = ingredient_value['id']
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            ingredients_amount = IngredientsAmount.objects.get_or_create(
                ingredient=ingredient,
                amount=ingredient_value['amount'],
            )
            validated_ingredients.append(ingredients_amount[0].id)
        return validated_ingredients

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data
