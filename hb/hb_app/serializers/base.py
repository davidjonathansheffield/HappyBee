from django.forms import model_to_dict
from rest_framework import serializers


class BaseSerializer(serializers.Serializer):

    requesting_user = None

    def get_requesting_user_member(self):
        if self.requesting_user is None:
            return None

        try:
            return self.requesting_user.member
        except AttributeError:
            return None

    @staticmethod
    def error_dict(e):
        return dict(
            success=False,
            errors=e.args,
        )

    @staticmethod
    def model_to_dict(model):
        return model_to_dict(model)

    @staticmethod
    def success_dict(**kwargs):
        return dict(
            success=True,
            **kwargs,
        )
