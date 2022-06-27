from django.db import models

from .base import BaseModel


class Team(BaseModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


__all__ = (
    'Team',
)
