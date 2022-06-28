from hb_app.models import Team
from .base import BaseSerializer


class TeamStatsSerializer(BaseSerializer):

    def validate(self, attrs):
        member = self.get_requesting_user_member()
        attrs['member'] = member
        return attrs

    def _get_avg_rating_and_team_name(self, member):
        qs = Team.objects.filter(members=member)
        avg_rating_by_team = qs.average_rating_by_team()
        requesting_user_team = qs[0]

        return avg_rating_by_team[requesting_user_team.id], requesting_user_team.name

    def create(self, validated_data):
        if validated_data['member'] is None:
            return dict(all_teams_average=Team.objects.all().average_all_teams())

        average_rating, team_name = self._get_avg_rating_and_team_name(validated_data['member'])

        return {
            f"{team_name} Average": average_rating,
        }


__all__ = (
    'TeamStatsSerializer',
)
