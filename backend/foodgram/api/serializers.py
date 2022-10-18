from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from recipes.models import Recipe, Tag
from users.serializers import UserActionGetSerializer


class TagSerializer(serializers.ModelSerializer):
    """Класс тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Класс рецептов."""
    author = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text',
                  'cooking_time')

    def create(self, validated_data):
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            name=validated_data['name'],
            text=validated_data['text'],
            cooking_time=validated_data['cooking_time'],
        )
        recipe.save()
        return recipe

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
