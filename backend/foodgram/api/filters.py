from django_filters.rest_framework import filters, FilterSet, NumberFilter

from recipes.models import Ingredient, Recipe, Tag


class IngredientSearchFilterSet(FilterSet):
    """Поиск по названию ингредиента."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilterSet(FilterSet):
    """Класс фильтрации рецептов."""
    author = NumberFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = NumberFilter(method='filter_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(favorite_recipe__user=user)
        if value == 0:
            return queryset.exclude(favorite_recipe__user=user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(recipe_in_shopping_cart__user=user)
        if value == 0:
            return queryset.exclude(recipe_in_shopping_cart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
