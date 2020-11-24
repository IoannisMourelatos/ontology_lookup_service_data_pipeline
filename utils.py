from urllib.parse import urlencode


def single_url_encode(text):
    result = urlencode({'url': text})
    return result[4:]


def double_url_encode(text):
    return single_url_encode(single_url_encode(text))
