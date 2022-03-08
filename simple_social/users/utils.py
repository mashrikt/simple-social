from urllib.parse import urlencode

from ..settings import ABSTRACT_API


def format_abstract_api_url(subdomain_type, params):
    subdomain = ABSTRACT_API[subdomain_type]['SUBDOMAIN']
    domain = ABSTRACT_API['DOMAIN']
    version = ABSTRACT_API['VERSION']
    api_key = ABSTRACT_API[subdomain_type]['API_KEY']
    params['api_key'] = api_key
    url = f'https://{subdomain}.{domain}/{version}/?{urlencode(params)}'
    return url
