# ruff: noqa: F811
import pytest
from fixtures import client_with_url  # noqa: F401
from requests import Response
from requests.exceptions import HTTPError


def test__handle_http_error(client_with_url):
    response = Response()
    response.status_code = 200
    try:
        client_with_url()._handle_http_error(response)
    except HTTPError:
        pytest.fail('Unexpected HTTPError raised')


def test_handle_response_raise_no_content(client_with_url):
    response = Response()
    response._content = b''
    response.status_code = 404
    with pytest.raises(HTTPError) as excinfo:
        client_with_url()._handle_response(response)
    assert excinfo.value.args[0] == '404 Client Error: None for url: None'


def test_handle_response_raise_no_content_and_401(client_with_url):
    response = Response()
    response._content = b''
    response.status_code = 401
    with pytest.raises(HTTPError) as excinfo:
        client_with_url()._handle_response(response)
    assert (
        excinfo.value.args[0]
        == '\nMake sure `CLIENT_WITH_URL_USERNAME` and `CLIENT_WITH_URL_PASSWORD` are set as environment variables or provided during initialization.'
    )


def test_handle_response_raise_with_content(client_with_url):
    response = Response()
    response._content = b'Custom error message'
    response.status_code = 400
    with pytest.raises(HTTPError) as excinfo:
        client_with_url()._handle_response(response)
    assert excinfo.value.args[0] == 'Custom error message'


def test_handle_response_raise_with_content_and_401(client_with_url):
    response = Response()
    response._content = b'Custom error message'
    response.status_code = 401
    with pytest.raises(HTTPError) as excinfo:
        client_with_url()._handle_response(response)
    assert (
        excinfo.value.args[0]
        == 'Custom error message\nMake sure `CLIENT_WITH_URL_USERNAME` and `CLIENT_WITH_URL_PASSWORD` are set as environment variables or provided during initialization.'
    )
