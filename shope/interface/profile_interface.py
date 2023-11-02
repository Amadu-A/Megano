"""Interface for profile app"""

from abc import abstractmethod

from profile_app.models import Profile
from auth_app.models import User


class IProfile:
    """IProfile class"""

    @abstractmethod
    def save(self, user: User) -> None:
        """Сохранить профайл."""
        pass
