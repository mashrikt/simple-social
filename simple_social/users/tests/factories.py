from django.contrib.auth import get_user_model
from factory import Faker, PostGenerationMethodCall
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'test_pass')
    is_active = True
    is_email_verified = True

    class Meta:
        model = User
