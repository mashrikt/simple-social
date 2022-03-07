from dj_rest_auth.registration.views import RegisterView as AuthRegisterView
from dj_rest_auth.serializers import UserDetailsSerializer


class RegisterView(AuthRegisterView):
    def get_response_data(self, user):
        return UserDetailsSerializer(user, context=self.get_serializer_context()).data
