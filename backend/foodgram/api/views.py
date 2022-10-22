from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilterSet
from api.serializers import (IngredientsAmountCreateRecipeSerializer,
                             IngredientSerializer, RecipeCreateSerializer,
                             RecipeSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, Ingredients_amount, Recipe,
                            Tag)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс работы с ингредиентами."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс работы с тэгами."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Класс работы с рецептами."""
    RESPONSE_DETAIL = {
        'detail': 'У вас недостаточно прав для выполнения данного действия.'
    }
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilterSet

    def creating_ingredients(self, request):
        ingredients = []
        request_ingredients = request.data['ingredients']
        for ingredient in request_ingredients:
            ingredient_obj = get_object_or_404(Ingredient, id=ingredient['id'])
            try:
                ingredients_amount = Ingredients_amount.objects.get(
                    ingredient=ingredient_obj,
                    amount=ingredient['amount']
                )
                ingredients.append(ingredients_amount.id)
            except:
                data = {
                    'ingredient': ingredient_obj.id,
                    'amount': ingredient['amount']
                }
                context = data
                serializer = IngredientsAmountCreateRecipeSerializer(
                    data=data,
                    context=context
                )
                if serializer.is_valid():
                    ingredients_amount = Ingredients_amount.objects.create(
                        ingredient=ingredient_obj,
                        amount=ingredient['amount']
                    )
                    ingredients_amount.save
                    ingredients.append(ingredients_amount.id)
                else:
                    status400 = status.HTTP_400_BAD_REQUEST
                    return 'Error', Response(serializer.errors,
                                             status=status400)
        request.data['ingredients'] = ingredients
        return None, request

    def create(self, request):
        request.data['author'] = request.user.id
        error, request = self.creating_ingredients(request)
        if error:
            return request
        context = {'request': self.request}
        serializer = RecipeCreateSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_author(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        author = recipe.author
        user = request.user
        if author == user:
            return recipe
        return False

    def partial_update(self, request, pk=None):
        recipe = self.is_author(request, pk)
        if recipe:
            request = self.request
            if 'ingredients' in request.data:
                error, request = self.creating_ingredients(request)
                if error:
                    return request
            context = {'request': request}
            serializer = RecipeCreateSerializer(
                recipe,
                data=request.data,
                context=context,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(self.RESPONSE_DETAIL, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        recipe = self.is_author(request, pk)
        if recipe:
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(self.RESPONSE_DETAIL, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post', 'delete'], detail=False,
            url_path='(?P<pk>[^/.]+)/favorite',
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        response_errors = {
            'POST': 'Вы уже добавили этот рецепт в избранное',
            'DELETE': 'Вы еще не добавили этот рецепт в избранное',
        }
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        favorite = Favorite.objects.filter(recipe=recipe, user=user)
        is_favorite = bool(favorite)
        if request.method == 'POST' and not is_favorite:
            favorite = Favorite(recipe=recipe, user=user)
            favorite.save()
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and is_favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        response = {'errors': response_errors[request.method]}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
