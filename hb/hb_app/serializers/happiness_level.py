from rest_framework import serializers

from hb_app.models import HappinessLevel
from .base import BaseSerializer


class SubmitHappinessSerializer(BaseSerializer):
    rating = serializers.IntegerField()

    @staticmethod
    def get_member(requesting_user):
        try:
            return requesting_user.member
        except AttributeError:
            member = None

        return member

    def validate(self, attrs):
        member = self.get_member(self.requesting_user)

        if member is None:
            raise ValueError("User is not on a team. Please request an admin place this user on a team.")

        attrs['team_member_id'] = member.id
        return attrs

    def create(self, validated_data):
        try:
            happiness_level = HappinessLevel.objects.record(
                team_member_id=validated_data.get('team_member_id'),
                rating=validated_data.get('rating'),
            )
        except ValueError as e:
            return {
                'errors': e.args,
                'success': False,
            }

        return {
            'created_at': happiness_level.created_at,
            'rating': happiness_level.rating,
            'success': True,
            'team_member_id': happiness_level.team_member_id,
        }
