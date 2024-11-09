# ruff: noqa: F811

import logging

import pytest
from fixtures import client, client_with_url, set_env_client_base_url  # noqa: F401


# Base client name tests
def test_base_client_name(client):
    assert client.base_client_name == 'client'


def test_base_client_name_other(client_with_url):
    assert client_with_url.base_client_name == 'client_with_url'


# Base url tests
def test_base_url(client_with_url):
    assert client_with_url.base_url == 'https://test.skillcorner'
    instance_of_client = client_with_url()
    assert instance_of_client.base_url == 'https://test.skillcorner'


def test_base_url_set_as_environment_variable(set_env_client_base_url, client):
    assert client.base_url is None
    instance_of_client = client()
    assert instance_of_client.base_url == 'https://test.skillcorner'


def test_base_url_not_set(client):
    assert client.base_url is None


def test_base_url_not_set_raise(client):
    with pytest.raises(KeyError):
        client()


# Log level tests
def test_response_log_level(set_env_client_base_url, client):
    instance_of_client = client()
    assert instance_of_client.response_log_level is None


def test_response_log_level_to_debug(set_env_client_base_url, client):
    instance_of_client = client(response_log_level=logging.DEBUG)
    assert instance_of_client.response_log_level == logging.DEBUG


def test_response_log_level_to_info(set_env_client_base_url, client):
    instance_of_client = client(response_log_level=logging.INFO)
    assert instance_of_client.response_log_level == logging.INFO
