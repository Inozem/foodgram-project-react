from django_filters.rest_framework import FilterSet, NumberFilter

from recipes.models import Recipe


class RecipeFilterSet(FilterSet):
    author = NumberFilter(field_name='author__id')

    class Meta:
        model = Recipe
        fields = ['id', 'author']
