from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import (CustomUserSerializer,
                               CustomTokenObtainPairSerializer,
                               CustomTokenObtainPairSerializer2)
from recipes.models import User


class CreateListRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class UserViewSet(CreateListRetrieveViewSet):
    """Создание пользователя"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False, url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenObtainPairView2(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer2
    # permission_classes = (IsAuthenticated,)
