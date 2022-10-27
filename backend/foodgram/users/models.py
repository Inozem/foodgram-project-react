from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс пользователя."""
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=254,
        verbose_name='Имя',
        blank=False,
    )
    last_name = models.CharField(
        max_length=254,
        verbose_name='Фамилия',
        blank=False,
    )


class Subscription(models.Model):
    """Класс для подписки на авторов рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
