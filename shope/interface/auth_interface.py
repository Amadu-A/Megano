from abc import abstractmethod

from auth_app.models import User


class IAuth:

    @abstractmethod
    def save(self, model: User) -> None:
        """Сохранить пользователя."""
        pass

    @abstractmethod
    def get_user_by_email(self, _email):
        """Получаем пользователя"""
        pass

    @abstractmethod
    def delete_user_by_email(self, _email):
        """Удаление пользователя по email"""
        pass
