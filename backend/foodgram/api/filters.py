from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter

from recipes.models import Recipe


class RecipeFilterSet(FilterSet):
    """Класс фильтрации рецептов."""
    author = NumberFilter(field_name='author__id')
    tags = CharFilter(field_name='tags__slug')
    is_favorited = NumberFilter(method='filter_is_favorited')

    def filter_is_favorited(self, queryset, name, value):
        if value == 1:
            return queryset.filter(favorite_recipe__user=self.request.user)
        elif value == 0:
            return queryset.exclude(favorite_recipe__user=self.request.user)

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited',)
