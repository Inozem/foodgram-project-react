# Generated by Django 3.2.15 on 2022-10-28 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_auto_20221028_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', to='recipes.Ingredients_amount', verbose_name='Ингредиенты'),
        ),
    ]
