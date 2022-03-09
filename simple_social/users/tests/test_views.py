from datetime import datetime, timedelta
import pytest
from django.urls import reverse
from faker import Faker
from rest_framework_simplejwt.state import token_backend

from .factories import User


fake = Faker()


class TestRegistration:
    @pytest.fixture
    def url(self):
        return reverse('api:auth:registration')

    @pytest.fixture
    def registration_data(self, password):
        data = {
            'email': fake.email(),
            'password1': password,
            'password2': password,
        }
        return data

    def test_user_registration_success(self, client, url, registration_data, password):
        response = client.post(url, registration_data)
        assert response.status_code == 201
        user = User.objects.get(id=response.data['pk'])
        assert user.check_password(password)
        assert user.is_active == True
        assert user.is_email_format_valid is None

    def test_password_mismatch(self, client, url, registration_data):
        registration_data['password2'] = fake.password()
        response = client.post(url, registration_data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == "The two password fields didn't match."
        created = User.objects.filter(email=registration_data['email']).exists()
        assert created == False

    def test_unique_email(self, client, url, user, registration_data):
        registration_data['email'] = user.email
        response = client.post(url, registration_data)
        assert response.status_code == 400
        assert response.data['email'][0] == 'A user is already registered with this e-mail address.'


class TestLogin:
    @pytest.fixture
    def url(self):
        return reverse('api:auth:login')

    def test_login_response(self, client, url, user, password):
        data = {
            'email': user.email,
            'password': password
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert response.data['user']['email'] == user.email
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data

    def test_login_access_token(self, client, url, user, password):
        data = {
            'email': user.email,
            'password': password
        }
        response = client.post(url, data)
        assert response.status_code == 200
        access_token = response.data['access_token']
        payload = token_backend.decode(access_token, True)
        assert payload['token_type'] == 'access'
        assert payload['user_id'] == user.id
        expires_at = datetime.fromtimestamp(payload['exp'])
        expected = datetime.now() + timedelta(minutes=5)
        # access token expiration should be 5 minutes
        assert abs(expected - expires_at) < timedelta(seconds=5)

    def test_login_refresh_token(self, client, url, user, password):
        data = {
            'email': user.email,
            'password': password
        }
        response = client.post(url, data)
        assert response.status_code == 200
        refresh_token = response.data['refresh_token']
        payload = token_backend.decode(refresh_token, True)
        assert payload['token_type'] == 'refresh'
        assert payload['user_id'] == user.id
        expires_at = datetime.fromtimestamp(payload['exp'])
        expected = datetime.now() + timedelta(days=1)
        # refresh token expiration should be 1 day
        assert abs(expected - expires_at) < timedelta(seconds=5)

    def test_wrong_email_login(self, client, url, user, password):
        data = {
            'email': fake.email(),
            'password': password
        }
        response = client.post(url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'

    def test_wrong_password_login(self, client, url, user):
        data = {
            'email': user.email,
            'password': fake.password()
        }
        response = client.post(url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'

    def test_inactive(self, client, url, user, password):
        user.is_active = False
        user.save()
        data = {
            'email': user.email,
            'password': password
        }
        response = client.post(url, data)
        assert response.status_code == 400

    def test_email_format_awaiting_verification(self, client, url, user, password):
        user.is_email_format_valid = None
        user.save()
        data = {
            'email': user.email,
            'password': password
        }
        response = client.post(url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'User email address format validation is not complete yet.'

    def test_email_format_invalid(self, client, url, user, password):
        user.is_email_format_valid = False
        user.save()
        data = {
            'email': user.email,
            'password': password
        }
        response = client.post(url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'User email address is invalid.'
