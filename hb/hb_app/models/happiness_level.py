from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from django.db import models

from .base import BaseModel, BaseManager


class HappinessLevelManager(BaseManager):

    @staticmethod
    def _validate_rating(rating):
        rating_setting = settings.RATING_SETTING
        if rating_setting.min > rating:
            raise ValueError(rating_setting.error(too_high=False))
        if rating_setting.max < rating:
            raise ValueError(rating_setting.error(too_high=True))

    def daily_happiness_level(self, team_member_id: int, rating: int) -> "HappinessLevel":
        """

        :param team_member_id: The id of the team member to register happiness for today.
        :param rating: The numeric rating for their happiness.  Validated based on RATING_SETTING in hb/settings.py.
        :return: Returns a happiness_level orm object for today's rating.
        :exception: If happiness_level is already registered, will throw a ValueError.
        """

        self._validate_rating(rating)

        happiness_level, created = self.get_or_create(
            team_member_id=team_member_id,
            created_at__date=timezone.now().date(),
        )

        if not created:
            raise ValueError("Happiness Level Already Recorded For Today.")

        return happiness_level


class HappinessLevel(BaseModel):
    team_member = models.ForeignKey("TeamMember", on_delete=models.CASCADE, related_name="levels")
    rating = models.IntegerField(
        validators=(
            MinValueValidator(
                limit_value=settings.RATING_SETTING.min,
                message=settings.RATING_SETTING.error(too_high=False),
            ),
            MaxValueValidator(
                limit_value=settings.RATING_SETTING.max,
                message=settings.RATING_SETTING.error(too_high=True),
            )
        )
    )

    objects = HappinessLevelManager()


__all__ = (
    'HappinessLevel',
)
