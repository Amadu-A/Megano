"""Команда создания заказов"""
from django.core.management import BaseCommand
from core.models.price import Price

import random
import datetime


def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))


class Command(BaseCommand):
    """ Добавление даты в модель цен """

    def handle(self, *args, **kwargs):
        """handle"""
        start = datetime.datetime(2022, 1, 1)
        end = datetime.datetime(2023, 10, 1)

        self.stdout.write('Добавляем цены в модель Price:')

        prices = Price.objects.all()
        for i_price in prices:
            i_price.date = random_date(start, end)
            i_price.save()
            self.stdout.write(f'В {i_price} добавлена дата {i_price.date}')

        self.stdout.write('Даты в цены добавлены:')
