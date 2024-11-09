import os

import pytest
from requests.packages.urllib3.util.retry import Retry

from fitrequest.client import FitRequest


class Client(FitRequest):
    base_client_name = 'client'


class ClientWithDocstringTemplate(FitRequest):
    base_url = 'https://test.skillcorner.fr'
    base_client_name = 'client_with_docstring_template'
    _docstring_template = 'Template of docstring used in every method.'
    _methods_binding = [
        {
            'name': 'get_items',
            'endpoint': '/items/',
        },
        {
            'name': 'get_item',
            'endpoint': '/items/{}/',
        },
        {
            'name': 'get_dosctring_set',
            'endpoint': '/with-docstring',
            'docstring': 'Template is ignored if set.',
        },
    ]


class ClientWithDocstringTemplateAndVariables(FitRequest):
    base_url = 'https://test.skillcorner.fr'
    base_client_name = 'client_with_docstring_template_and_variables'
    _docstring_template = (
        'Calling endpoint: {endpoint}\nDocs URL anchor: {docs_url_anchor}'
    )
    _methods_binding = [
        {
            'name': 'get_items',
            'endpoint': '/items/',
            'docs_url_anchor': '/items/items_list',
        },
        {
            'name': 'get_item',
            'endpoint': '/items/{}/',
            'docs_url_anchor': '/items/item_read',
            'docstring': 'Template is ignored if set.',
        },
        {
            'name': 'get_with_no_docstring_variable_but_dosctring_set',
            'endpoint': '/no-doctsring-variable/with-docstring',
            'docstring': 'Its own docstring.',
        },
    ]


class ClientWithMethods(FitRequest):
    base_url = 'https://test.skillcorner.fr'
    base_client_name = 'client_with_methods'
    _methods_binding = [
        {
            'name': 'get_default_args',
            'endpoint': '/default-args/',
        },
        {
            'name': 'get_docstring',
            'endpoint': '/docstring/',
            'docstring': 'Here is a description of the method.',
        },
        {
            'name': 'get_doc_none_if_empty',
            'endpoint': '/docstring/empty',
            'docstring': '',
        },
        {
            'name': 'get_items',
            'endpoint': '/items/',
        },
        {
            'name': 'get_item',
            'endpoint': '/items/{}',
            'resource_name': 'item_id',
        },
        {
            'name': 'get_no_raise_on_status',
            'endpoint': '/raise-on-status/false',
            'raise_for_status': False,
        },
        {
            'name': 'get_raise_for_status',
            'endpoint': '/raise-on-status/true',
            'raise_for_status': True,
        },
        {
            'name': 'get_value_in_response_key',
            'endpoint': '/response-key/',
            'response_key': 'data',
        },
        {
            'name': 'get_with_extra_params',
            'endpoint': '/extra-params/',
            'extra_params': ['extra_param_1', 'extra_param_2'],
        },
        {
            'name': 'get_with_save_method_explicitly',
            'create_save_method': True,
            'endpoint': '/save-method/',
        },
        {
            'name': 'get_without_save_method',
            'create_save_method': False,
            'endpoint': '/no-save-method/',
        },
    ]


class ClientWithURL(FitRequest):
    base_url = 'https://test.skillcorner'
    base_client_name = 'client_with_url'


class ClientWithURLandCredentialsEnv(FitRequest):
    base_url = 'https://test.skillcorner'
    base_client_name = 'client_with_url_and_credentials_env'
    _environment_password_key = 'CUSTOM_PASSWORD_KEY'
    _environment_username_key = 'CUSTOM_USERNAME_KEY'


class ClientWithURLandRetry(FitRequest):
    base_url = 'https://test.skillcorner'
    base_client_name = 'client_with_url_and_retry'
    _retry = Retry(
        total=3, backoff_factor=0.6, status_forcelist=Retry.RETRY_AFTER_STATUS_CODES
    )


@pytest.fixture()
def set_env_client_base_url():
    os.environ['CLIENT_BASE_URL'] = 'https://test.skillcorner'
    yield
    os.environ.pop('CLIENT_BASE_URL')


@pytest.fixture()
def set_env_credentials():
    os.environ['CLIENT_WITH_URL_USERNAME'] = 'skcr'
    os.environ['CLIENT_WITH_URL_PASSWORD'] = 'goal'
    yield
    os.environ.pop('CLIENT_WITH_URL_USERNAME')
    os.environ.pop('CLIENT_WITH_URL_PASSWORD')


@pytest.fixture()
def client():
    return Client


@pytest.fixture()
def client_with_docstring_template():
    return ClientWithDocstringTemplate


@pytest.fixture()
def client_with_docstring_template_and_variables():
    return ClientWithDocstringTemplateAndVariables


@pytest.fixture()
def client_with_methods():
    return ClientWithMethods


@pytest.fixture()
def client_with_url():
    return ClientWithURL


@pytest.fixture()
def client_with_url_and_credentials_env():
    return ClientWithURLandCredentialsEnv


@pytest.fixture()
def client_with_url_and_retry():
    return ClientWithURLandRetry
