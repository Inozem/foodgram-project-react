from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework.response import Response

from users.models import Subscription, User
from users.serializers import (CustomUserSerializer, UserActionGetSerializer,
                               ChangePasswordSerializer)


class CreateListRetrieveDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserViewSet(CreateListRetrieveDestroyViewSet):
    """Класс регистрации и работы с пользователями и подписками на авторов"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return UserActionGetSerializer
        return CustomUserSerializer

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

    @action(detail=False, url_path='subscribtions',
            permission_classes=[IsAuthenticated])
    def subscribtions(self, request):
        authors = User.objects.filter(follower__user=request.user)
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=False,
            url_path='(?P<pk>[^/.]+)/subscribe',
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        response_errors = {
            'POST': ('Вы уже подписаны на этого автора или '
                     'пытаетеcь подписаться на самого себя'),
            'DELETE': 'Вы не подписаны на этого автора',
        }
        author = get_object_or_404(User, pk=pk)
        user = request.user
        subscription = Subscription.objects.filter(author=author, user=user)
        is_subscribed = bool(subscription)
        if request.method == 'POST' and author != user and not is_subscribed:
            subscription = Subscription(author=author, user=user)
            subscription.save()
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and is_subscribed:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        response = {'errors': response_errors[request.method]}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
