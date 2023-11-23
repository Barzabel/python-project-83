import validators
from urllib.parse import urlparse


def is_validat_url(url):
    errors = {}
    if len(url) > 255:
        errors['lenghth'] = 'the address is too long, more than 255 characters'
    if not validators.url(url):
        errors['worng_url'] = 'incorrect url format'
    return errors


def get_clear_url(url):
    pars_url = urlparse(url)
    return "{}://{}".format(pars_url.scheme, pars_url.netloc)
