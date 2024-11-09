# ruff: noqa: F811
import pytest
from fixtures import client_with_url  # noqa: F401
from fitrequest.method_generator import RequestMethod


def test_check_request_get_almost_too_long_valid(client_with_url):
    try:
        client_with_url()._check_request(
            method=RequestMethod.get,
            url='https://test.skillcorner/bar',
            params={'foo': 'b' * 4060},
        )
    except ValueError:
        pytest.fail('Unexpected ValueError')


def test_check_request_get_valid(client_with_url):
    try:
        client_with_url()._check_request(
            method=RequestMethod.get, url='https://test.skillcorner/bar', params=None
        )
    except ValueError:
        pytest.fail('Unexpected ValueError')


def test_check_request_post_valid(client_with_url):
    try:
        client_with_url()._check_request(
            method=RequestMethod.post, url='https://test.skillcorner/bar', params=None
        )
    except ValueError:
        pytest.fail('Unexpected ValueError')


def test_check_request_get_a_bit_too_long_raise(client_with_url):
    with pytest.raises(ValueError):
        client_with_url()._check_request(
            method=RequestMethod.get,
            url='https://test.skillcorner/bar',
            params={'foo': 'b' * 4062},
        )


def test_check_request_get_way_too_long_raise(client_with_url):
    with pytest.raises(ValueError):
        client_with_url()._check_request(
            method=RequestMethod.get,
            url='https://test.skillcorner/bar',
            params={'foo': 'b' * 15000},
        )
