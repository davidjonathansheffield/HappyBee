from dataclasses import dataclass

from rest_framework.response import Response

from .base import BaseAuthAPIView

from hb_app.models import HappinessLevel


class SubmitHappinessAPIView(BaseAuthAPIView):

    @staticmethod
    def get_member(request):
        try:
            return request.user.member
        except AttributeError:
            member = None

        return member

    def post(self, request):
        member = self.get_member(request)
        if member is None:
            return Response({"error": "User is not on a team. Please request an admin place this user on a team."})

        happiness_level = HappinessLevel.objects.record(
            team_member_id=member.id,
        )

        return Response({"derp": "derp"})


__all__ = (
    'SubmitHappinessAPIView',
)
