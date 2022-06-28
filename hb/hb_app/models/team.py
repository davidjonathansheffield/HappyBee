from collections import defaultdict

from django.db import models

from .team_member import TeamMember
from .base import BaseModel, BaseQuerySet, BaseManager


class TeamQuerySet(BaseQuerySet):

    def average_rating_by_team(self) -> dict[int, float]:
        """
        :param self: Is a queryset of Teams
        :return: A dictionary, key is team_id, value is average ratings.
        """

        team_ids = self.values_list('id', flat=True)
        team_members = TeamMember.objects.filter(
            team_id__in=team_ids
        ).annotate_average_happiness()

        rating_list_by_team = defaultdict(list)
        for team_member in team_members:
            if team_member.average_happiness is not None:
                rating_list_by_team[team_member.team_id].append(team_member.average_happiness)

        avg_rating_by_team = defaultdict(float)
        for team in rating_list_by_team:
            avg_rating_by_team[team] = sum(rating_list_by_team[team]) / len(rating_list_by_team[team])

        return avg_rating_by_team

    def average_all_teams(self):
        average_rating_by_team = self.average_rating_by_team()

        num_teams = 0
        sum_avg_rating = 0
        for team_id in average_rating_by_team:
            num_teams += 1
            sum_avg_rating += average_rating_by_team[team_id]

        return sum_avg_rating / num_teams


class TeamManager(BaseManager):
    pass


class Team(BaseModel):
    name = models.CharField(max_length=150)

    objects = TeamManager.from_queryset(TeamQuerySet)()

    def __str__(self):
        return self.name


__all__ = (
    'Team',
)
