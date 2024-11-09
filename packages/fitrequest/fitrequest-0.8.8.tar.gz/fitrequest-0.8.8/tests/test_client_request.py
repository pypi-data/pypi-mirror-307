# ruff: noqa: F811
import logging
from unittest.mock import patch

import pytest
from fixtures import client_with_url  # noqa: F401
from requests import Response, Session
from requests.exceptions import HTTPError

from fitrequest.method_generator import RequestMethod


def test_get_request_default_args(client_with_url):
    response = Response()
    response.status_code = 200
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url()._request(method=RequestMethod('GET'), endpoint='ok/')
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
        )


def _test_get_request_with_response_log_level(
    client_with_url, caplog, response_log_level
):
    caplog.set_level(logging.DEBUG)
    expected_logs = response_log_level, 'Response from client_with_url'
    response = Response()
    response.status_code = 200
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url(response_log_level=response_log_level)._request(
            method=RequestMethod('GET'), endpoint='ok/'
        )
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
        )
        assert (caplog.records[-1].levelno, caplog.records[-1].message) == expected_logs


def test_get_request_with_response_log_level_debug(client_with_url, caplog):
    _test_get_request_with_response_log_level(client_with_url, caplog, logging.DEBUG)


def test_get_request_with_response_log_level_info(client_with_url, caplog):
    _test_get_request_with_response_log_level(client_with_url, caplog, logging.INFO)


def test_get_request_without_response_log_level(client_with_url, caplog):
    caplog.set_level(logging.INFO)
    expected_logs = [
        (
            logging.WARNING,
            'Cannot retrieve package version, either your package is not named '
            f'{client_with_url.base_client_name} (as your base_client_name attribute), or it is not installed.',
        ),
        (logging.INFO, 'Sending GET request to: https://test.skillcorner/ok/'),
    ]
    response = Response()
    response.status_code = 200
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url()._request(method=RequestMethod('GET'), endpoint='ok/')
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
        )
        assert (caplog.records[0].levelno, caplog.records[0].message) == expected_logs[
            0
        ]
        assert (caplog.records[1].levelno, caplog.records[1].message) == expected_logs[
            1
        ]


def test_get_request_with_raise_for_status_default(client_with_url):
    response = Response()
    response.status_code = 500
    with patch.object(Session, 'request', return_value=response) as mock, pytest.raises(
        HTTPError
    ):
        client_with_url()._request(method=RequestMethod('GET'), endpoint='raise/')
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
        )


def test_get_request_with_raise_for_status_false(client_with_url):
    response = Response()
    response.status_code = 500
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url()._request(
            method=RequestMethod('GET'), endpoint='ok/', raise_for_status=False
        )
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
        )


def test_get_request_with_raise_for_status_true(client_with_url):
    response = Response()
    response.status_code = 500
    with patch.object(Session, 'request', return_value=response) as mock, pytest.raises(
        HTTPError
    ):
        client_with_url()._request(
            method=RequestMethod('GET'), endpoint='raise/', raise_for_status=True
        )
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
        )


def test_get_request_with_single_value_params(client_with_url):
    response = Response()
    response.status_code = 200
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url()._request(
            method=RequestMethod('GET'),
            endpoint='ok/',
            params={'foo': 'bar', 'baz': 'quux'},
        )
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
            params={'foo': 'bar', 'baz': 'quux'},
        )


def test_get_request_with_list_in_params(client_with_url):
    response = Response()
    response.status_code = 200
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url()._request(
            method=RequestMethod('GET'),
            endpoint='ok/',
            params={'foo': 'bar', 'param_list': [1, 2, 3, 4]},
        )
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
            params={'foo': 'bar', 'param_list': '1,2,3,4'},
        )


def test_get_request_with_list_in_params_as_str(client_with_url):
    response = Response()
    response.status_code = 200
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url()._request(
            method=RequestMethod('GET'),
            endpoint='ok/',
            params={'foo': 'bar', 'param_list': '1,2,3,4'},
        )
        mock.assert_called_once_with(
            method='GET',
            url='https://test.skillcorner/ok/',
            params={'foo': 'bar', 'param_list': '1,2,3,4'},
        )


def test_get_request_with_wrong_params_type_list(client_with_url):
    with pytest.raises(AttributeError):
        client_with_url()._request(
            method=RequestMethod('GET'), endpoint='ok/', params=[{'foo': 'bar'}]
        )


def test_get_request_with_wrong_params_type_str(client_with_url):
    with pytest.raises(AttributeError):
        client_with_url()._request(
            method=RequestMethod('GET'), endpoint='ok/', params='1,2,3,4'
        )


def test_post_request_with_data(client_with_url):
    data = {'key': 'value'}
    response = Response()
    response.status_code = 200
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url()._request(
            method=RequestMethod('POST'), endpoint='ok/', data=data
        )
        mock.assert_called_once_with(
            method='POST',
            url='https://test.skillcorner/ok/',
            data={'key': 'value'},
        )


def test_post_request_with_json(client_with_url):
    _json = [1, 2, 3]
    response = Response()
    response.status_code = 200
    with patch.object(Session, 'request', return_value=response) as mock:
        client_with_url()._request(
            method=RequestMethod('POST'), endpoint='ok/', json=_json
        )
        mock.assert_called_once_with(
            method='POST',
            url='https://test.skillcorner/ok/',
            json=[1, 2, 3],
        )
