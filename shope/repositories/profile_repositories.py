"""Repositories of Profile app"""

from beartype import beartype
from interface.profile_interface import IProfile
from profile_app.models import Profile


class ProfileRepository(IProfile):
    """ProfileRepository"""

    @beartype
    def save(self, model: Profile) -> None:
        """Сохранить профайл."""

        model.save()
