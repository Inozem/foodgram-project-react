from django.contrib import admin

from recipes.models import Ingredient, Ingredients_amount, Recipe, Tag

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Ingredients_amount)
