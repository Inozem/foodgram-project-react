from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework.response import Response

from users.models import Subscription, User
from users.serializers import (CustomUserSerializer, ChangePasswordSerializer,)


class CreateListRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class UserViewSet(CreateListRetrieveViewSet):
    """Класс регистрации и работы с пользователями"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='set_password',
            permission_classes=[IsAuthenticated])
    def set_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = self.request.user.email
            current_password = serializer.validated_data['password']
            new_password = serializer.validated_data['new_password']
            user = get_object_or_404(User, email=email)
            if user.check_password(current_password):
                user.password = new_password
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False,
            url_path='(?P<pk>[^/.]+)/subscribe',
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = request.user
        subscription = Subscription.objects.filter(author=author, user=user)
        is_subscribed = bool(subscription)
        if author != user and not is_subscribed:
            subscription = Subscription(author=author, user=user)
            subscription.save()
            return Response(status=status.HTTP_201_CREATED)
        response = {'errors': ('Вы уже подписаны на этого автора или '
                               'пытаетель подписаться на самого себя.')}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
