from hb_app.enums import RequestMethodEnum
from hb_app.serializers import TeamStatsSerializer
from .base import BaseAPIView


class TeamStatsAPIView(BaseAPIView):
    allowable_request_methods = {RequestMethodEnum.GET}
    serializer_class = TeamStatsSerializer


__all__ = (
    'TeamStatsAPIView',
)
