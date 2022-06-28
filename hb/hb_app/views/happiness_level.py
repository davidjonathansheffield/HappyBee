from hb_app.enums import RequestMethodEnum
from hb_app.serializers import SubmitHappinessSerializer
from .base import BaseAuthAPIView


class SubmitHappinessAPIView(BaseAuthAPIView):
    allowable_request_methods = {RequestMethodEnum.POST}
    serializer_class = SubmitHappinessSerializer


__all__ = (
    'SubmitHappinessAPIView',
)
