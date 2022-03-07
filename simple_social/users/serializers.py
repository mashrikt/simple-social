
from dj_rest_auth.serializers import LoginSerializer as AuthLoginSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class LoginSerializer(AuthLoginSerializer):

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.ValidationError(msg)

        if not user.is_email_verified:
            msg = _('User email address is not verified.')
            raise exceptions.ValidationError(msg)
