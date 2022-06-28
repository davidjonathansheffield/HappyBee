import random
from collections import defaultdict
from unittest import TestCase

from hb_app.models import Team, TeamMember, HappinessLevel


class TeamQuerySetTests(TestCase):

    def setUp(self) -> None:
        self.teams = [
            Team.objects.create(name=f'Team #{i}')
            for i in range(1, 4)
        ]

        self.ratings_by_team = defaultdict(list)

        for team in self.teams:
            for i in range(3):
                tm = TeamMember.objects.create_with_test_user(team=team)
                random_rating = random.randint(1, 10)

                HappinessLevel.objects.record(
                    team_member_id=tm.id,
                    rating=random_rating,
                )
                self.ratings_by_team[team.id].append(random_rating)

    def _count_ratings(self):
        sum_all_ratings = 0
        num_ratings = 0
        for team_id in self.ratings_by_team:
            sum_all_ratings += sum(self.ratings_by_team[team_id])
            num_ratings += len(self.ratings_by_team[team_id])

        return sum_all_ratings, num_ratings

    def test_average_all_teams(self):
        calculated_avg_all_teams = Team.objects.all().average_all_teams()
        sum_all_ratings, num_ratings = self._count_ratings()

        # Rounding necessary for float imprecision
        self.assertEqual(
            round(sum_all_ratings / num_ratings, 2),
            round(calculated_avg_all_teams, 2),
        )

    def test_average_rating_by_team(self):
        calculated_avg_rating_by_team = Team.objects.all().average_rating_by_team()
        for team_id in self.ratings_by_team:
            rating_list = self.ratings_by_team[team_id]
            rating_list_avg = sum(rating_list) / len(rating_list)
            calc_rating_avg = calculated_avg_rating_by_team[team_id]

            self.assertEqual(rating_list_avg, calc_rating_avg)
