from beartype import beartype

from auth_app.models import User
from interface.auth_interface import IAuth


class AuthRepository(IAuth):

    @beartype
    def save(self, model: User) -> None:
        model.save()

    @beartype
    def get_user_by_email(self, _email: str) -> User:
        """Получаем пользователя"""
        return User.objects.get(email=_email)

    @beartype
    def delete_user_by_email(self, _email: str):
        """Удаляем пользователя"""
        return User.objects.get(email=_email).delete()
