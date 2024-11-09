# ruff: noqa: F811
from fixtures import client_with_url, client_with_url_and_retry  # noqa: F401
from requests import Session


def test_session_property_is_instanciated(client_with_url):
    value = client_with_url().session
    assert isinstance(value, Session)


def test_session_attribute_is_None(client_with_url):
    client = client_with_url()
    assert client._session is None


def test_session_attribute_is_set_after_first_call(client_with_url):
    client = client_with_url()
    assert isinstance(client.session, Session)


def test_session_auth(client_with_url):
    client = client_with_url()
    client._ensure_authenticated()
    expected_client = client_with_url()
    expected_client._ensure_authenticated()
    expected = expected_client._auth
    assert client.session.auth == expected


def test_session_headers(client_with_url):
    client = client_with_url()
    expected = {'User-Agent': 'fitrequest.client_with_url.{version}'}
    assert client.session.headers == expected


def test_session_retry_not_set(client_with_url):
    client = client_with_url()
    assert client.session.adapters['http://'].max_retries.total == 0
    assert client.session.adapters['https://'].max_retries.total == 0


def test_session_retry_init(client_with_url_and_retry):
    client = client_with_url_and_retry()
    assert client.session.adapters['http://'].max_retries.total == 3
    assert client.session.adapters['https://'].max_retries.total == 3


def test_session_retry(client_with_url_and_retry):
    client = client_with_url_and_retry()
    assert client.session.adapters['http://'].max_retries.total == 3
    assert client.session.adapters['https://'].max_retries.total == 3
