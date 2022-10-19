from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter

from recipes.models import Recipe


class RecipeFilterSet(FilterSet):
    """Класс фильтрации рецептов."""
    author = NumberFilter(field_name='author__id')
    tags = CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
