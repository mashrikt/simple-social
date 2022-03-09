import pytest
import requests_mock
from faker import Faker

from ..tests.factories import UserFactory
from ...users.utils import format_abstract_api_url
from ...users.tasks import validate_email, get_user_location_data, has_user_registered_on_a_holiday


fake = Faker()

class TestValidateEmail:

    @pytest.fixture
    def user(self, password):
        return UserFactory(password=password, is_email_format_valid=None)

    @pytest.fixture
    def url(self, user):
        params = {'email': user.email}
        return format_abstract_api_url('EMAIL_VALIDATION', params)

    @pytest.fixture
    def response_data(self, user):
        data = {
            'email': user.email,
            'is_valid_format': {
                'value': True,
            }
        }
        return data

    @pytest.fixture
    def invalid_response_data(self, response_data):
        response_data['is_valid_format']['value'] = False
        return response_data

    def test_valid_email(self, user, url, response_data):
        with requests_mock.Mocker() as m:
            m.get(url, json=response_data)
            validate_email(user.email)
        user.refresh_from_db()
        assert user.is_email_format_valid == True

    def test_invalid_email(self, user, url, invalid_response_data):
        with requests_mock.Mocker() as m:
            m.get(url, json=invalid_response_data)
            validate_email(user.email)
        user.refresh_from_db()
        assert user.is_email_format_valid == False


class TestHasUserRegisteredOnAHoliday:

    @pytest.fixture
    def user(self, geolocation_data, password):
        registration_ip, is_registration_ip_routable = geolocation_data['ip_address'], True
        return UserFactory(password=password, registration_ip=registration_ip,
            is_registration_ip_routable=is_registration_ip_routable)

    @pytest.fixture
    def user_ip_invalid(self, user):
        user.is_registration_ip_routable = False
        user.save()
        return user

    @pytest.fixture
    def url(self, user):
        params = {'ip_address': user.registration_ip}
        return format_abstract_api_url('IP_GEOLOCATION', params)

    def test_get_data(self, user, url, geolocation_data):
        with requests_mock.Mocker() as m:
            m.get(url, json=geolocation_data)
            get_user_location_data(user.email)
        user.refresh_from_db()
        assert user.location_data == geolocation_data

    def test_ip_not_routable(self, user_ip_invalid):
        get_user_location_data(user_ip_invalid.email)
        user_ip_invalid.refresh_from_db()
        assert user_ip_invalid.location_data == {}


class TestGetUserLocationData:

    @pytest.fixture
    def user(self, password, geolocation_data):
        return UserFactory(password=password, location_data=geolocation_data)

    @pytest.fixture
    def url(self, user, geolocation_data):
        params = {
            'country': geolocation_data['country_code'],
            'year': user.date_joined.year,
            'month': user.date_joined.month,
            'day': user.date_joined.day,
        }
        return format_abstract_api_url('HOLIDAYS', params)

    @pytest.fixture
    def response_data(self, user):
        data = [
            {
                'name': 'Holiday everyday',
            }
        ]
        return data

    def test_holiday(self, user, url, response_data):
        with requests_mock.Mocker() as m:
            m.get(url, json=response_data)
            has_user_registered_on_a_holiday(user.email)
        user.refresh_from_db()
        assert user.is_date_joined_local_holiday == True

    def test_not_holiday(self, user, url):
        with requests_mock.Mocker() as m:
            m.get(url, json={})
            has_user_registered_on_a_holiday(user.email)
        user.refresh_from_db()
        assert user.is_date_joined_local_holiday == False
