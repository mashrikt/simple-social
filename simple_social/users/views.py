from dj_rest_auth.registration.views import RegisterView as AuthRegisterView
from dj_rest_auth.serializers import UserDetailsSerializer


class RegisterView(AuthRegisterView):

    def get_response_data(self, user):
        # change serializer to only return user related data and no tokens
        return UserDetailsSerializer(user, context=self.get_serializer_context()).data


    def perform_create(self, serializer):
        # overriding to stop logging in the user
        user = serializer.save(self.request)
        user.validate_email()
        user.enhance_geolocation()
        return user
