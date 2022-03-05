import os
from urllib.parse import urlsplit, urlunsplit


def url_change(url: str) -> str:
    """
    Подмена url
    :param url: URL
    :return: URL с подменным на GRAFANA_URL доменом
    """

    url_splitted = urlsplit(url)

    url_splitted = url_splitted._replace(netloc=os.getenv('GRAFANA_URL', 'localhost'))

    return urlunsplit(url_splitted)
