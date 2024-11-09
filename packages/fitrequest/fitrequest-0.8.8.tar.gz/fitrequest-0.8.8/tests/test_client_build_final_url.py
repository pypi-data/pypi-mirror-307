# ruff: noqa: F811
import pytest
from fixtures import client_with_url  # noqa: F401


def test_build_final_url_valid(client_with_url):
    client = client_with_url()
    endpoint = 'endpoint'
    expected = 'https://test.skillcorner/endpoint'
    value = client._build_final_url(endpoint=endpoint)
    assert value == expected


def test_build_final_url_valid_with_starting_slash(client_with_url):
    client = client_with_url()
    endpoint = '/endpoint'
    expected = 'https://test.skillcorner/endpoint'
    value = client._build_final_url(endpoint=endpoint)
    assert value == expected


def test_build_final_url_valid_only_trailing_slash(client_with_url):
    client = client_with_url()
    endpoint = 'endpoint/'
    expected = 'https://test.skillcorner/endpoint/'
    value = client._build_final_url(endpoint=endpoint)
    assert value == expected


def test_build_final_url_valid_trailing_slash(client_with_url):
    client = client_with_url()
    endpoint = '/endpoint/'
    expected = 'https://test.skillcorner/endpoint/'
    value = client._build_final_url(endpoint=endpoint)
    assert value == expected


def test_build_final_url_invalid_type(client_with_url):
    client = client_with_url()
    endpoint = 150
    with pytest.raises(AttributeError):
        client._build_final_url(endpoint=endpoint)
