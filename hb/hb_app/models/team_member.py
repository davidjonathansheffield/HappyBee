from django.contrib.auth.models import User
from django.db import models

from .base import BaseModel, BaseManager, BaseQuerySet

from .happiness_level import HappinessLevel


class TeamMemberQuerySet(BaseQuerySet):

    def annotate_latest_happiness(self):
        return self.annotate(
            latest_happiness=models.Subquery(
                HappinessLevel.objects.filter(
                    team_member_id=models.OuterRef('id')
                ).order_by('-created_at').values('rating')[:1]
            )
        )

    def annotate_average_happiness(self):
        return self.annotate(
            average_happiness=models.Avg('levels__rating'),
        )


class TeamMemberManager(BaseManager):
    pass


class TeamMember(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="members")

    objects = TeamMemberManager.from_queryset(TeamMemberQuerySet)()


__all__ = (
    'TeamMember',
)
