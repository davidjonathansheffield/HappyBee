from django.contrib.auth.models import User
from django.test import TestCase
from freezegun import freeze_time

from hb_app.models import HappinessLevel, Team, TeamMember


class HappinessLevelRecordUnitTests(TestCase):

    def setUp(self) -> None:
        self.team = Team.objects.create(name="Test Team")
        self.team_member = TeamMember.objects.create(
            team=self.team,
            user=User.objects.create_user(username=f'Test User', password='12345')
        )

    def test_record_basic(self):
        happiness_level = HappinessLevel.objects.record(
            team_member_id=self.team_member.id, rating=5,
        )

        self.assertEqual(
            happiness_level.team_member_id,
            self.team_member.id,
        )

        self.assertEqual(
            happiness_level.rating,
            5,
        )

    def test_record_fails_twice_in_same_day(self):
        HappinessLevel.objects.record(
            team_member_id=self.team_member.id, rating=5,
        )
        with self.assertRaises(ValueError) as e:
            HappinessLevel.objects.record(
                team_member_id=self.team_member.id, rating=5,
            )

    def test_record_succeeds_twice_in_different_days(self):
        with freeze_time("2022-01-01"):
            HappinessLevel.objects.record(
                team_member_id=self.team_member.id, rating=5,
            )

        with freeze_time("2022-01-02"):
            HappinessLevel.objects.record(
                team_member_id=self.team_member.id, rating=5,
            )

    def test_record_succeeds_two_different_team_members(self):
        other_user = User.objects.create_user(username="Other User", password="12345")
        other_team_member = TeamMember.objects.create(team=self.team, user=other_user)
        HappinessLevel.objects.record(
            team_member_id=self.team_member.id,
            rating=5,
        )

        HappinessLevel.objects.record(
            team_member_id=other_team_member.id,
            rating=6,
        )
