# ruff: noqa: F811
import inspect
from unittest.mock import mock_open, patch

import orjson
import pytest
import requests_mock
from fixtures import (  # noqa: F401
    client_with_docstring_template,
    client_with_docstring_template_and_variables,
    client_with_methods,
)
from requests import Session
from requests.exceptions import HTTPError


def test_methods_binding_call_method(client_with_methods):
    expected = {
        'items': [
            {'item_id': 1, 'item_name': 'ball'},
            {'item_id': 2, 'item_name': 'gloves'},
        ]
    }
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://test.skillcorner.fr/items/',
            headers={'Content-Type': 'application/json'},
            json={
                'items': [
                    {'item_id': 1, 'item_name': 'ball'},
                    {'item_id': 2, 'item_name': 'gloves'},
                ]
            },
        )
        response = client_with_methods().get_items()
    assert response == expected


def test_methods_binding_with_docstring_template(client_with_docstring_template):
    expected = 'Template of docstring used in every method.'
    value_1 = client_with_docstring_template().get_item.__doc__
    value_2 = client_with_docstring_template().get_items.__doc__
    assert value_1 == value_2 == expected


def test_methods_binding_with_docstring_template_ignored(
    client_with_docstring_template,
):
    expected = 'Template is ignored if set.'
    value = client_with_docstring_template().get_dosctring_set.__doc__
    assert value == expected


def test_methods_binding_with_docstring_and_variables_template(
    client_with_docstring_template_and_variables,
):
    expected = 'Calling endpoint: /items/\nDocs URL anchor: /items/items_list'
    value = client_with_docstring_template_and_variables().get_items.__doc__
    assert value == expected


def test_methods_binding_with_docstring_template_and_variables_template_ignored(
    client_with_docstring_template_and_variables,
):
    expected = 'Template is ignored if set.'
    value = client_with_docstring_template_and_variables().get_item.__doc__
    assert value == expected


def test_methods_binding_with_docstring_template_and_docstring_but_no_variables(
    client_with_docstring_template_and_variables,
):
    expected = 'Its own docstring.'
    value = client_with_docstring_template_and_variables().get_with_no_docstring_variable_but_dosctring_set.__doc__
    assert value == expected


def test_methods_binding_call_method_with_id(client_with_methods):
    expected = {'item_id': 1, 'item_name': 'ball'}
    item_id = 32
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            f'https://test.skillcorner.fr/items/{item_id}',
            headers={'Content-Type': 'application/json'},
            json={'item_id': 1, 'item_name': 'ball'},
        )
        response = client_with_methods().get_item(item_id)
    assert response == expected


def test_methods_binding_call_method_with_endpoint_arg(client_with_methods):
    with patch.object(Session, 'request') as mock:
        client_with_methods().get_item(32, endpoint='gitlab.com/test-project')
        mock.assert_called_once_with(
            method='GET', url='https://test.skillcorner.fr/items/32', params=None
        )


def test_methods_binding_call_method_with_request_method_arg(client_with_methods):
    with patch.object(Session, 'request') as mock:
        client_with_methods().get_item(25, method='PUT')
        mock.assert_called_once_with(
            method='GET', url='https://test.skillcorner.fr/items/25', params=None
        )


def test_methods_binding_with_extra_params(client_with_methods):
    expected = '(self, extra_param_1: str, extra_param_2: str, params: dict = None, raise_for_status: bool = True, **kwargs)'
    value = str(inspect.signature(client_with_methods.get_with_extra_params))
    assert value == expected


def test_methods_binding_docstring_None(client_with_methods):
    value = client_with_methods().get_default_args.__doc__
    assert value is None


def test_methods_binding_docstring_empty(client_with_methods):
    value = client_with_methods().get_doc_none_if_empty.__doc__
    assert value is None


def test_methods_binding_docstring(client_with_methods):
    expected = 'Here is a description of the method.'
    value = client_with_methods().get_docstring.__doc__
    assert value == expected


def test_methods_binding_with_response_key(client_with_methods):
    expected = [
        {'user_id': 1, 'user_name': 'Motta'},
        {'user_id': 2, 'user_name': 'Busquets'},
    ]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://test.skillcorner.fr/response-key/',
            headers={'Content-Type': 'application/json'},
            json={
                'data': [
                    {'user_id': 1, 'user_name': 'Motta'},
                    {'user_id': 2, 'user_name': 'Busquets'},
                ],
                'metadata': {'total_count': 2},
            },
        )
        response = client_with_methods().get_value_in_response_key()
    assert response == expected


def test_methods_binding_with_response_key_but_not_dict(client_with_methods):
    expected = [
        {
            'data': [
                {'user_id': 1, 'user_name': 'Motta'},
                {'user_id': 2, 'user_name': 'Busquets'},
            ]
        }
    ]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://test.skillcorner.fr/response-key/',
            headers={'Content-Type': 'application/json'},
            json=[
                {
                    'data': [
                        {'user_id': 1, 'user_name': 'Motta'},
                        {'user_id': 2, 'user_name': 'Busquets'},
                    ]
                }
            ],
        )
        response = client_with_methods().get_value_in_response_key()
    assert response == expected


def test_methods_binding_with_no_raise_on_status(client_with_methods):
    expected = b''
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://test.skillcorner.fr/raise-on-status/false',
            status_code=404,
        )
        response = client_with_methods().get_no_raise_on_status()
    assert response == expected


def test_methods_binding_with_raise_on_status_404(client_with_methods):
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://test.skillcorner.fr/raise-on-status/true',
            status_code=404,
        )
        with pytest.raises(HTTPError):
            client_with_methods().get_raise_for_status()


def test_methods_binding_with_raise_on_status_500(client_with_methods):
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://test.skillcorner.fr/raise-on-status/true',
            status_code=500,
        )
        with pytest.raises(HTTPError):
            client_with_methods().get_raise_for_status()


def test_methods_binding_with_random_kwargs(client_with_methods):
    expected = b''
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://test.skillcorner.fr/default-args/',
        )
        response = client_with_methods().get_default_args(kwarg1='foo', kwarg2='bar')
    assert response == expected


def test_methods_binding_with_save_method_explicit(client_with_methods):
    body = {'best_team_name': 'Paris Saint-Germain'}
    filepath = 'test_save.json'
    expected = orjson.dumps(body, option=orjson.OPT_INDENT_2)
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://test.skillcorner.fr/save-method/',
            headers={'Content-Type': 'application/json'},
            json=body,
        )
        open_mock = mock_open()
        with patch('builtins.open', open_mock, create=True):
            client_with_methods().save_with_save_method_explicitly(filepath=filepath)
    open_mock.assert_called_with(filepath, 'xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_methods_binding_with_save_method_implicit(client_with_methods):
    body = {'item_id': 17, 'item_name': 'ball'}
    item_id = 17
    filepath = 'test_save_items.json'
    expected = orjson.dumps(body, option=orjson.OPT_INDENT_2)
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            f'https://test.skillcorner.fr/items/{item_id}',
            headers={'Content-Type': 'application/json'},
            json={'item_id': 17, 'item_name': 'ball'},
        )
        open_mock = mock_open()
        with patch('builtins.open', open_mock, create=True):
            client_with_methods().save_item(item_id=item_id, filepath=filepath)
    open_mock.assert_called_with(filepath, 'xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_methods_binding_without_save_method(client_with_methods):
    with pytest.raises(AttributeError):
        client_with_methods().save_without_save_method()


def test_methods_binding_with_unknown_positional_arg(client_with_methods):
    with pytest.raises(TypeError):
        client_with_methods().get_default_args(
            'first_arg_is_params', 'second_arg_is_raise_for_status', 'unknown_arg'
        )


def test_methods_binding_wrong_methods_name(client_with_methods):
    with pytest.raises(
        AttributeError,
        match="ClientWithMethods' object has no attribute/method 'get_and_save_items'. Did you mean 'save_items'?",
    ):
        client_with_methods().get_and_save_items()
