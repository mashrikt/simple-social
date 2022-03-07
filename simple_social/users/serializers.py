from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.serializers import LoginSerializer as AuthLoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer as AuthRegisterSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip
from rest_framework import exceptions, serializers


class LoginSerializer(AuthLoginSerializer):

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.ValidationError(msg)

        if not user.is_email_verified:
            msg = _('User email address is not verified.')
            raise exceptions.ValidationError(msg)


class RegisterSerializer(AuthRegisterSerializer):

    def save(self, request):
        """
        overriding to add client_ip
        reference: https://github.com/iMerica/dj-rest-auth/blob/master/dj_rest_auth/registration/serializers.py#L194
        """
        adapter = get_adapter()
        user = adapter.new_user(request)

        client_ip, _ = get_client_ip(request)
        user.registration_ip=client_ip

        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        user.save()
        return user
