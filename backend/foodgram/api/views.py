from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from api.filters import RecipeFilterSet
from api.serializers import RecipeSerializer, TagSerializer
from recipes.models import Recipe, Tag


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
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilterSet
    filterset_fields = ('id', 'author')

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
            serializer = self.serializer_class(
                recipe,
                data=request.data,
                context=context,
                partial=True
            )
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(self.RESPONSE_DETAIL, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        recipe = self.is_author(request, pk)
        if recipe:
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(self.RESPONSE_DETAIL, status=status.HTTP_403_FORBIDDEN)
