from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """Класс регистрации пользователей"""
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


class UserActionGetSerializer(UserSerializer):
    """Класс получения данных пользователей"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, value):
        user = self.context['request'].user
        if user.is_authenticated:
            subscription = Subscription.objects.filter(author=value, user=user)
            return subscription.exists()
        return False  # Если пользователь аноним


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    """Класс получения рецептов авторов, на которых подписан."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')


class SubscriptionSerializer(UserActionGetSerializer):
    """Класс получения данных подписок на авторов."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, value):
        serialized_recipes = []
        request = self.context.get('request')
        context = {'request': request}
        recipes = Recipe.objects.filter(author=value)
        for recipe in recipes:
            serialized_recipe = SubscriptionRecipeSerializer(recipe,
                                                             context=context)
            serialized_recipes.append(serialized_recipe.data)
        return serialized_recipes

    def get_recipes_count(self, value):
        return len(Recipe.objects.filter(author=value))


class ChangePasswordSerializer(UserSerializer):
    """Класс изменения пароля у пользователя"""
    current_password = serializers.CharField(source='password', required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password')

    def validate_new_password(self, value):
        return make_password(value)
