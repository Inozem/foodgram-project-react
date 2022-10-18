from colorfield.fields import ColorField
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Класс ингредиента."""
    name = models.CharField(
        max_length=254,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=150,
        verbose_name='Единица измерения',
    )

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Ingredients_amount(models.Model):
    """Класс количества ингредиентов."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент'
    )
    amount = models.FloatField(verbose_name='Количество')

    def __str__(self):
        return (f'{self.ingredient.name} - '
                f'{self.amount} {self.ingredient.measurement_unit}')

    class Meta:
        verbose_name = 'Кол-во ингредиентов'
        verbose_name_plural = 'Кол-во ингредиентов'


class Tag(models.Model):
    """Класс тэгов."""
    name = models.CharField(
        max_length=254,
        verbose_name='Название',
        unique=True
    )
    color = ColorField(default='#FF0000', unique=True)
    slug = models.SlugField(max_length=150, verbose_name='Ссылка', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


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
    ingredients = models.ManyToManyField(
        Ingredients_amount,
        related_name='ingredients_amount',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тэги',
    )
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
