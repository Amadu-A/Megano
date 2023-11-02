"""Команда создания характеристик товаров"""
from typing import Any, Optional
from django.core.management import BaseCommand

from catalog_app.models import (
    CharacteristicType,
    CharacteristicValue,
    CharacteristicProduct,
    Category,
    Product
)


class Command(BaseCommand):
    """Создание характеристики"""

    def handle(self, *args: Any, **options: Any) -> str | None:
        """handle"""

        # Типы характеристик
        category = Category.objects.get(pk=1)
        self.stdout.write('Начало создания типов характеристик')
        data_list = [
            ('Диагональ', category),
            ('Производитель', category),
            ('Тип матрицы', category),
        ]
        res = [CharacteristicType.objects.get_or_create(name=name, category=category)
               for name, category in data_list]

        self.stdout.write('Созданы типы характеристик:')
        for i_obj in res:
            self.stdout.write(str(i_obj))
        self.stdout.write('Конец создания типов характеристик')

        # Значения характеристик

        self.stdout.write('Начало создания значений характеристик')
        data_list = [
            ('Диагональ', '27"'),
            ('Диагональ', '30"'),
            ('Производитель', 'Samsung'),
            ('Производитель', 'LG'),
            ('Тип матрицы', 'TN+Film'),
            ('Тип матрицы', 'IPS'),
        ]
        res = [
            CharacteristicValue.objects.get_or_create(
                characteristic_type=CharacteristicType.objects.get(name=name),
                value=value) for name, value in data_list
        ]

        self.stdout.write('Значения типов характеристик заполнены:')
        for i_obj in res:
            self.stdout.write(str(i_obj))

    # Назначение характеристик продуктам
        self.stdout.write('Начало присвоения характеристик продуктам')

        data_list = [
            (Product.objects.get(pk=1), CharacteristicValue.objects.get(pk=1)),
            (Product.objects.get(pk=1), CharacteristicValue.objects.get(pk=3)),
            (Product.objects.get(pk=1), CharacteristicValue.objects.get(pk=1)),
            (Product.objects.get(pk=2), CharacteristicValue.objects.get(pk=1)),
            (Product.objects.get(pk=2), CharacteristicValue.objects.get(pk=4)),
            (Product.objects.get(pk=2), CharacteristicValue.objects.get(pk=6)),
        ]

        res = [
            CharacteristicProduct.objects.get_or_create(
                product=i_product,
                characteristic_value=i_value) for i_product, i_value in data_list
        ]

        self.stdout.write('Присвоены значения характеристик продуктам:')
        for i_obj in res:
            self.stdout.write(str(i_obj))

        self.stdout.write('Конец заполнения характеристик')
