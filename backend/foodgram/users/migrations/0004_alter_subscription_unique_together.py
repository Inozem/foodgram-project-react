# Generated by Django 3.2.15 on 2022-10-27 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20221025_1235'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('user', 'author')},
        ),
    ]