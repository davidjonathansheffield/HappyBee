import random
from collections import defaultdict

from django.contrib.auth.models import User
from django.db import models

from .base import BaseModel, BaseManager, BaseQuerySet

from .happiness_level import HappinessLevel


class TeamMemberQuerySet(BaseQuerySet):

    def annotate_average_happiness(self):
        return self.annotate(
            average_happiness=models.Avg('levels__rating'),
        )

    def annotate_latest_happiness(self):
        return self.annotate(
            latest_happiness=models.Subquery(
                HappinessLevel.objects.filter(
                    team_member_id=models.OuterRef('id')
                ).order_by('-created_at').values('rating')[:1]
            )
        )

    def team_members_by_happiness_levels(self):
        team_members = self.annotate_latest_happiness()
        team_members_by_happiness_levels = defaultdict(int)

        for team_member in team_members:
            team_members_by_happiness_levels[team_member.latest_happiness] += 1

        return team_members_by_happiness_levels


class TeamMemberManager(BaseManager):

    def create_with_test_user(self, **kwargs):
        random_name = "".join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(25)])
        return self.create(
            user=User.objects.create_user(username=random_name, password='12345'),
            **kwargs,
        )


class TeamMember(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="members")

    objects = TeamMemberManager.from_queryset(TeamMemberQuerySet)()


__all__ = (
    'TeamMember',
)
