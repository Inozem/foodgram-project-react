from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter

from recipes.models import Recipe


class RecipeFilterSet(FilterSet):
    """Класс фильтрации рецептов."""
    author = NumberFilter(field_name='author__id')
    tags = CharFilter(field_name='tags__slug')
    is_favorited = NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = NumberFilter(method='filter_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(favorite_recipe__user=user)
        elif value == 0:
            return queryset.exclude(favorite_recipe__user=user)
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(recipe_in_shopping_cart__user=user)
        elif value == 0:
            return queryset.exclude(recipe_in_shopping_cart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
