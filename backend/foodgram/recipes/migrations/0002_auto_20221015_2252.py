# Generated by Django 3.2.15 on 2022-10-15 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-created',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='pub_date',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
    ]
