import pytest


@pytest.fixture
def geolocation_data():
    return {
        'ip_address': '166.171.248.255',
        'city': 'Modesto',
        'city_geoname_id': 5373900,
        'region': 'California',
        'region_iso_code': 'CA',
        'region_geoname_id': 5332921,
        'postal_code': '95353',
        'country': 'United States',
        'country_code': 'US',
        'country_geoname_id': 6252001,
        'country_is_eu': False,
        'continent': 'North America',
        'continent_code': 'NA',
        'continent_geoname_id': 6255149,
        'longitude': -120.997,
        'latitude': 37.6393,
        'security': {
            'is_vpn': False
        },
        'timezone': {
            'name': 'America/Los_Angeles',
            'abbreviation': 'PST',
            'gmt_offset': -8,
            'current_time': '07:10:37',
            'is_dst': False
        },
        'flag': {
            'emoji': '🇺🇸',
            'unicode': 'U+1F1FA U+1F1F8',
            'png': 'https://static.abstractapi.com/country-flags/US_flag.png',
            'svg': 'https://static.abstractapi.com/country-flags/US_flag.svg'
        },
        'currency': {
            'currency_name': 'USD',
            'currency_code': 'USD'
        },
    }
