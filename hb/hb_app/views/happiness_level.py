from serializers.happiness_level import SubmitHappinessSerializer
from .base import BaseAuthAPIView


class SubmitHappinessAPIView(BaseAuthAPIView):
    serializer_class = SubmitHappinessSerializer


__all__ = (
    'SubmitHappinessAPIView',
)
