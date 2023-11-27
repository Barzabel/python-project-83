import validators
from urllib.parse import urlparse


def validate_url(url):
    errors = []
    if not validators.url(url):
        errors.append(('Некорректный URL', 'danger'))
    if len(url) > 255:
        errors.append(('Error! Url length > 255', 'danger'))
    return errors


def extract_domain(url):
    parsed_url = urlparse(url)
    return "{}://{}".format(parsed_url.scheme, parsed_url.netloc)
