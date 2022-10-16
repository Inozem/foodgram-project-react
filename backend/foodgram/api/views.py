from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from api.serializers import RecipeSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    RESPONSE_DETAIL = {
        'detail': 'У вас недостаточно прав для выполнения данного действия.'
    }
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

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
            context = {'request': self.request}
            serializer = self.serializer_class(recipe, data=request.data, context=context, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(self.RESPONSE_DETAIL, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        pass
