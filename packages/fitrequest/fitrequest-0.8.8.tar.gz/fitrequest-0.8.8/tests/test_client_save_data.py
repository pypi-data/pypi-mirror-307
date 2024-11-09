# ruff: noqa: F811
from unittest.mock import mock_open, patch

import orjson
from io import BytesIO
import xml.etree.ElementTree as ET
import pytest
from fixtures import client_with_url  # noqa: F401


def test_save_data_bytes(client_with_url):
    filepath = 'bytes_saved.txt'
    data = b'test data'
    expected = b'test data'

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True):
        client_with_url()._save_data(filepath, data)
    open_mock.assert_called_with(filepath, 'xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_data_json(client_with_url):
    filepath = 'test.json'
    data = {'id': 35, 'area': 'AFC', 'name': 'Asian Cup'}
    expected = orjson.dumps(data, option=orjson.OPT_INDENT_2)

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True):
        client_with_url()._save_data(filepath, data)
    open_mock.assert_called_with(filepath, 'xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_data_element(client_with_url):
    filepath = 'test.xml'
    raw_data = '<root>data</root>'
    data = ET.fromstring(raw_data)
    expected = bytes(
        f"<?xml version='1.0' encoding='utf-8'?>\n{raw_data}", encoding='utf-8'
    )

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True):
        client_with_url()._save_data(filepath, data)
    open_mock.assert_called_with(filepath, 'xb')
    open_mock.return_value.write.assert_called_once_with(expected)


def test_save_data_bytesio(client_with_url):
    filepath = 'test.csv'
    data = b'A,B\r\n1,2\r\n3,4\r\n'

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True):
        client_with_url()._save_data(filepath, BytesIO(data))
    open_mock.assert_called_with(filepath, 'xb')
    open_mock.return_value.write.assert_called_once_with(data)


def test_save_data_invalid_path(client_with_url):
    with pytest.raises(FileNotFoundError):
        client_with_url()._save_data('/invalid/unknown/path/test/test.json', '')


def test_save_data_file_already_exists(client_with_url):
    filepath_already_taken = '.gitignore'
    warning_message_if_side_effect = 'erased by test_save_data_file_already_exists'
    with pytest.raises(FileExistsError):
        client_with_url()._save_data(
            filepath_already_taken, warning_message_if_side_effect
        )


def test_save_data_invalid_format(client_with_url):
    filepath = 'test_file'
    data = {1, 2, 3}

    open_mock = mock_open()
    with patch('builtins.open', open_mock, create=True), pytest.raises(TypeError):
        client_with_url()._save_data(filepath, data)
    open_mock.assert_called_with(filepath, 'xb')
