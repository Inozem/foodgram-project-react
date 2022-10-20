# Generated by Django 3.2.15 on 2022-10-17 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20221018_0240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='recipes.Tag', verbose_name='Тэги'),
        ),
    ]