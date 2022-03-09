from faker import Faker
import pytest
from rest_framework.test import APIClient

from .users.tests.factories import UserFactory

fake = Faker()


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def password():
    return fake.password()


@pytest.fixture
def user(password):
    return UserFactory(password=password)


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user)
    return client


@pytest.fixture
def other_user(password):
    return UserFactory(password=password)


@pytest.fixture
def other_auth_client(other_user, client):
    client.force_authenticate(other_user)
    return client


@pytest.fixture(params=['client', 'other_auth_client'])
def other_client(request):
    return request.getfixturevalue(request.param)
