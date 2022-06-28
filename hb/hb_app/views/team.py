from enums import RequestMethodEnum
from serializers.team import TeamStatsSerializer
from views.base import BaseAPIView


class TeamStatsAPIView(BaseAPIView):
    allowable_request_methods = {RequestMethodEnum.GET}
    serializer_class = TeamStatsSerializer


__all__ = (
    'TeamStatsAPIView',
)
