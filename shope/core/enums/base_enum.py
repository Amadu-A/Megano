""" Базовый класс enum"""
from enum import Enum, EnumType


class ChoicesMeta(EnumType):
    """Мета класс, дополняющий базовый Enum"""

    @property
    def choices(cls):
        """choices."""
        res = [(instance.name, instance.value) for instance in cls]  # type: ignore
        return res


class Choices(Enum, metaclass=ChoicesMeta):
    """Дополняет базовый Enum"""

    def __str__(self) -> str:
        """Строковое представление"""
        return str(self.value)
