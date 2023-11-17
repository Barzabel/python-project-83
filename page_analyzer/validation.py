import re


def is_validat_url(url):
    errors = {}
    url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$" # noqa E501
    if len(url) > 255:
        errors['lenghth'] = 'the address is too long, more than 255 characters'
    if re.match(url_pattern, url) is None:
        errors['worng_url'] = 'incorrect url format'
    return errors
