from django.contrib.auth.models import User
from django.db import models

from .base import BaseModel


class TeamMember(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="members")


__all__ = (
    'TeamMember',
)
