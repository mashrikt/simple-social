from django.db import transaction
from dj_rest_auth.registration.views import RegisterView as AuthRegisterView
from dj_rest_auth.serializers import UserDetailsSerializer


class RegisterView(AuthRegisterView):

    def get_response_data(self, user):
        # change serializer to only return user related data and no tokens
        return UserDetailsSerializer(user, context=self.get_serializer_context()).data

    def trigger_user_data_collection(self, user):
        user.validate_email()
        user.enhance_geolocation()


    def perform_create(self, serializer):
        # overriding to stop logging in the user
        user = serializer.save(self.request)
        # on_commit used to ensure that the celery tasks are invoked after db transaction is commited successfully
        # reference: https://docs.djangoproject.com/en/4.0/topics/db/transactions/#performing-actions-after-commit
        transaction.on_commit(lambda: self.trigger_user_data_collection(user))
        return user
