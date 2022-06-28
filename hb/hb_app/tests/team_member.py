from django.contrib.auth.models import User
from django.test import TestCase
from freezegun import freeze_time

from hb_app.models import HappinessLevel, Team, TeamMember


class TeamMemberQuerySetTests(TestCase):

    def setUp(self) -> None:
        self.team = Team.objects.create(name="Test Team")
        self.team_member = TeamMember.objects.create(
            team=self.team,
            user=User.objects.create_user(username=f'Test User', password='12345')
        )

    def _record_over_three_dates(self):
        with freeze_time("2022-01-01"):
            HappinessLevel.objects.record(
                team_member_id=self.team_member.id, rating=5,
            )

        with freeze_time("2022-01-02"):
            HappinessLevel.objects.record(
                team_member_id=self.team_member.id, rating=6,
            )

        with freeze_time("2022-01-04"):
            HappinessLevel.objects.record(
                team_member_id=self.team_member.id, rating=7,
            )

    def test_annotate_latest_happiness(self):
        self._record_over_three_dates()

        team_member = TeamMember.objects.filter(
            id=self.team_member.id,
        ).annotate_latest_happiness()[0]

        self.assertEqual(
            team_member.latest_happiness,
            7,
        )

    def test_annotate_average_happiness(self):
        self._record_over_three_dates()

        team_member = TeamMember.objects.filter(
            id=self.team_member.id,
        ).annotate_average_happiness()[0]

        self.assertEqual(
            team_member.average_happiness,
            6.0,
        )
