
from rest_framework import serializers

from hb_app.models import HappinessLevel
from .base import BaseSerializer


class SubmitHappinessSerializer(BaseSerializer):
    rating = serializers.IntegerField()

    def validate(self, attrs):
        member = self.get_requesting_user_member()

        if member is None:
            raise ValueError("Requesting User Is Not On A Team. Please Ask An Admin To Place This User On A Team.")

        attrs['team_member_id'] = member.id
        return attrs

    def create(self, validated_data):
        try:
            happiness_level = HappinessLevel.objects.record(
                team_member_id=validated_data.get('team_member_id'),
                rating=validated_data.get('rating'),
            )
        except ValueError as e:
            return self.error_dict(e)

        return self.success_dict(**self.model_to_dict(happiness_level))

    def update(self, instance, validated_data):
        raise NotImplementedError
