import re
import validators


def is_validat_url(url):
    errors = {}
    if len(url) > 255:
        errors['lenghth'] = 'the address is too long, more than 255 characters'
    if not validators.url(url):
        errors['worng_url'] = 'incorrect url format'
    return errors