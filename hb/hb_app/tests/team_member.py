from django.test import TestCase
from freezegun import freeze_time

from hb_app.models import HappinessLevel, Team, TeamMember


class TeamMemberQuerySetTests(TestCase):

    def setUp(self) -> None:
        self.team = Team.objects.create(name="Test Team")
        self.team_member = TeamMember.objects.create_with_test_user(
            team=self.team,
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

    def test_team_members_by_happiness_levels(self):
        other_team_members = [
            TeamMember.objects.create_with_test_user(
                team=self.team,
            )
            for _ in range(4)
        ]

        HappinessLevel.objects.record(
            team_member_id=self.team_member.id,
            rating=1,
        )

        for idx, team_member in enumerate(other_team_members):
            HappinessLevel.objects.record(
                team_member_id=team_member.id,
                rating=idx+2,
            )

        # An additional TeamMember that has not recorded
        TeamMember.objects.create_with_test_user(team=self.team)

        self.assertDictEqual(
            TeamMember.objects.filter(team=self.team).team_members_by_happiness_levels(),
            {
                1: 1,
                2: 1,
                3: 1,
                4: 1,
                5: 1,
                None: 1,  # Team Member that has never recorded
            }
        )
