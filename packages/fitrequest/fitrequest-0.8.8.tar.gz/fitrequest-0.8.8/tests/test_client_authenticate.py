# ruff: noqa: F811
from unittest import TestCase

import boto3
import pytest
from fixtures import (  # noqa: F401
    client_with_url,
    client_with_url_and_credentials_env,
    set_env_credentials,
)
from moto import mock_aws
from requests.auth import HTTPBasicAuth

from fitrequest.utils import AWSSecret


def test_authenticate_basic(client_with_url):
    client = client_with_url()
    client._ensure_authenticated()
    assert client._auth == HTTPBasicAuth('', '')


def test_authenticate_with_env(set_env_credentials, client_with_url):
    expected = HTTPBasicAuth('skcr', 'goal')
    client = client_with_url()
    client._ensure_authenticated()
    value = client._auth
    assert value == expected


def test_authenticate_with_no_arg(client_with_url):
    with pytest.raises(TypeError):
        client = client_with_url()
        client._ensure_authenticated()
        client._authenticate()


class TestSKCRUtilsSecret(TestCase):
    @mock_aws
    def test_get_ssm_secret(self):
        ssm = boto3.client('ssm', region_name='eu-central-1')
        ssm_value = 'this is it!'
        ssm.put_parameter(
            Name='/foo/bar',
            Description='A test parameter',
            Value=ssm_value,
            Type='SecureString',
        )
        self.assertEqual(
            AWSSecret(**{'type': 'ssm', 'path': '/foo/bar'}).value,
            ssm_value,
        )

    @mock_aws
    def test_get_secretsmanager_secret(self):
        secretsmanager = boto3.client('secretsmanager', region_name='eu-central-1')
        secretsmanager_value = 'this is it!'
        secretsmanager.create_secret(Name='/foo/bar', SecretString=secretsmanager_value)
        self.assertEqual(
            AWSSecret(**{'type': 'secretsmanager', 'path': '/foo/bar'}).value,
            secretsmanager_value,
        )
