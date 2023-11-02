"""Команда создания заказов"""
from django.core.management import BaseCommand

from order_app.models import Order
from auth_app.models import User


class Command(BaseCommand):
    """Создание заказов """

    def handle(self, *args, **kwargs):
        """handle"""

        self.stdout.write('Созданы типы характеристик:')
        data_list = [
            (User.objects.get(pk=2),
             'Novosibirsk',
             'Lenin str 458/1',
             '15650.0'
             ),
            (User.objects.get(pk=2),
             'Angarsk',
             '130 str 127',
             '14670.0'
             ),
            (User.objects.get(pk=3),
             'Omsk',
             'K Marks str 4/8',
             '2470.0'
             ),
            (User.objects.get(pk=2),
             'Irkutsk',
             'Gagarin str 34-8',
             '3670.0'
             ),
            (User.objects.get(pk=3),
             'Omsk',
             'K Marks str 4/8',
             '2470.0'
             ),
            (User.objects.get(pk=4),
             'Ekaterinburg',
             'Gagarin str 27-6',
             '15650.0'
             ),
        ]
        res = [Order.objects.get_or_create(
            user=user,
            city=city,
            address=address,
            amount=amount
        )
            for user, city, address, amount in data_list]

        self.stdout.write('Созданы заказы:')
        for i_obj in res:
            self.stdout.write(str(i_obj))
        self.stdout.write('Конец создания заказов')
