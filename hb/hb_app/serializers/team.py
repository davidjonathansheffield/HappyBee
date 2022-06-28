from hb_app.models import Team, TeamMember

from .base import BaseSerializer


class TeamStatsSerializer(BaseSerializer):

    @staticmethod
    def _get_avg_rating_and_team(member):
        qs = Team.objects.filter(members=member)
        avg_rating_by_team = qs.average_rating_by_team()
        requesting_user_team = qs[0]

        return avg_rating_by_team[requesting_user_team.id], requesting_user_team

    def validate(self, attrs):
        member = self.get_requesting_user_member()
        attrs['member'] = member
        return attrs

    def create(self, validated_data):

        if validated_data['member'] is None:
            return dict(all_teams_average=Team.objects.all().average_all_teams())

        average_rating, team = self._get_avg_rating_and_team(validated_data['member'])

        member_count_by_level = TeamMember.objects.filter(team=team).team_members_by_happiness_levels()

        return {
            team.name: dict(
                average=average_rating,
                member_count_by_level=member_count_by_level,
            ),
        }


__all__ = (
    'TeamStatsSerializer',
)
