from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseAPIView(APIView):
    """
    A base interface for all APIViews.
    """
    authentication_classes = [TokenAuthentication]


class BaseAuthAPIView(BaseAPIView):
    """
    A base authentication required APIView.
    """
    permission_classes = [IsAuthenticated]


__all__ = (
    'BaseAPIView',
    'BaseAuthAPIView',
)
