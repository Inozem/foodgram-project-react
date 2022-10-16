from django.db import models

from users.models import User


class Recipe(models.Model):
    """Класс рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creator',
        verbose_name='Автор'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    # image = models.TextField(verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст')
    # ingredients = models.ForeignKey(Ingredients_in_recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Ингредиенты')
    # tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tags', verbose_name='Тэги')
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
