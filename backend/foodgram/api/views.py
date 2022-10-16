from django.shortcuts import render
from rest_framework import mixins, status, viewsets

from api.serializers import RecipeSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
