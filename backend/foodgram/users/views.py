from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import Subscription, User
from users.serializers import (CustomUserSerializer, UserActionGetSerializer,
                               SubscriptionSerializer)


class CustomUserViewSet(UserViewSet):
    """Класс регистрации и работы с пользователями и подписками на авторов"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        context = {'request': self.request}
        serializer = UserActionGetSerializer(request.user, context=context)
        return Response(serializer.data)

    @action(detail=False, url_path='subscriptions',
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        authors = User.objects.filter(author__user=request.user)
        paginator = PageNumberPagination()
        result_pages = paginator.paginate_queryset(queryset=authors,
                                                   request=request)
        context = {'request': self.request}
        serializer = SubscriptionSerializer(result_pages, context=context,
                                            many=True)
        return paginator.get_paginated_response(serializer.data)

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
            request = self.request
            context = {'request': request}
            serializer = SubscriptionSerializer(author, context=context,)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and is_subscribed:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        response = {'errors': response_errors[request.method]}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
