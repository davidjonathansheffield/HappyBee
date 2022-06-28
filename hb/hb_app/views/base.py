from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseAPIView(APIView):
    """
    A base interface for all APIViews.
    """
    authentication_classes = [TokenAuthentication]
    renderer_classes = [JSONRenderer]
    serializer_class = None

    def post(self, request):
        if self.serializer_class is None:
            raise NotImplementedError

        serializer = self.serializer_class(data=request.data)
        serializer.requesting_user = request.user
        if serializer.is_valid():
            return Response(serializer.save())

        raise ValueError("Invalid arguments passed to API Endpoint.")


class BaseAuthAPIView(BaseAPIView):
    """
    A base authentication required APIView.
    """
    permission_classes = [IsAuthenticated]


__all__ = (
    'BaseAPIView',
    'BaseAuthAPIView',
)
