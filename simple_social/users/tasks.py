import logging
import requests
from django.contrib.auth import get_user_model
from requests.exceptions import RequestException

from .utils import format_abstract_api_url
from ..celery import app

User = get_user_model()
logger = logging.getLogger(__name__)


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def validate_email(email):
    params = {'email': email}
    url = format_abstract_api_url('EMAIL_VALIDATION', params)
    response = requests.get(url)
    response.raise_for_status()
    is_email_valid = response.json()['is_valid_format']['value']
    User.objects.filter(email__iexact=email).update(is_email_format_valid=is_email_valid)


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def get_user_location_data(email):
    user = User.objects.get(email__iexact=email)
    ip_address = str(user.registration_ip)
    is_ip_routable = user.is_registration_ip_routable
    if not is_ip_routable:
        logger.warning(f"User {user.email} IP address is not routable. So their geolocation data can't be fetched")
        return
    params = {'ip_address': ip_address}
    url = format_abstract_api_url('IP_GEOLOCATION', params)
    response = requests.get(url)
    response.raise_for_status()
    location_data = response.json()
    user.location_data = location_data
    user.save()


@app.task(autoretry_for=(RequestException,), retry_backoff=True)
def has_user_registered_on_a_holiday(email):
    user = User.objects.get(email__iexact=email)
    country_code = user.location_data.get('country_code')
    if not country_code:
        logger.warning(f"User {user.email}'s country_code is not available."
            f"Can't fetch info on whether registration day was a local holiday.")
        return
    params = {
        'country': country_code,
        'year': user.date_joined.year,
        'month': user.date_joined.month,
        'day': user.date_joined.day,
    }
    url = format_abstract_api_url('HOLIDAYS', params)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    is_holiday = bool(data and data[0].get('name'))
    user.is_date_joined_local_holiday = is_holiday
    user.save()
