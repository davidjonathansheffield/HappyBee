from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from hb_app.enums import RequestMethodEnum


class BaseAPIView(APIView):
    """
    A base interface for all APIViews.
    """
    authentication_classes = [TokenAuthentication]
    renderer_classes = [JSONRenderer]
    serializer_class = None
    allowable_request_methods = set()

    @classmethod
    def validate_method(cls, method: RequestMethodEnum):
        if method.value not in {
            allowed_method.value
            for allowed_method in cls.allowable_request_methods
        }:
            return False, f"Method '{method.value}' not allowed."
        else:
            return True, None

    def validate_serializer_class(self):
        if self.serializer_class is None:
            raise NotImplementedError("Serializer Class Must Be Set in APIView.")

    def get(self, request, *args, **kwargs):
        method_allowed, error = self.validate_method(RequestMethodEnum.GET)
        if not method_allowed:
            return Response(error)

        self.validate_serializer_class()

        serializer = self.serializer_class(data=kwargs)
        serializer.requesting_user = request.user
        if serializer.is_valid():
            return Response(serializer.save())

        raise ValueError("Invalid arguments passed to API Endpoint.")

    def post(self, request):
        method_allowed, error = self.validate_method(RequestMethodEnum.POST)
        if not method_allowed:
            return Response(error)

        self.validate_serializer_class()

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
