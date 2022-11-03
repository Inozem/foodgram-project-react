import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Импорт ингредиентов в БД"""
    help = 'Импорт ингредиентов в БД из .csv файла'

    def handle(self, *args, **options):
        with open('static/data/ingredients.csv', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                Ingredient.objects.create(name=row[0], measurement_unit=row[1])
