from django.contrib import admin

from recipes.models import Ingredient, IngredientsAmount, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    """Класс рецептов."""
    list_display = ('name', 'author', 'get_favorites_count')
    list_filter = ('author', 'name', 'tags')

    def get_favorites_count(self, obj):
        return obj.favorite_recipe.count()

    get_favorites_count.short_description = (
        'Кол-во человек добавивших в избранное'
    )


class IngredientAdmin(admin.ModelAdmin):
    """Класс ингредиентов."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientsAmount)
