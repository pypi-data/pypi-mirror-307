# ruff: noqa: F811
import orjson
import pytest
from defusedxml.ElementTree import fromstring, tostring
from fixtures import client_with_url  # noqa: F401
from requests import Response
from requests.exceptions import HTTPError


def test_handle_response_empty_response(client_with_url):
    response = Response()
    response.status_code = 200
    assert client_with_url()._handle_response(response) is None


def test_handle_response_csv_response(client_with_url):
    response = Response()
    response.status_code = 200
    response.headers = {'Content-Type': 'text/csv'}
    csv_bytes = b'A,B\r\n1,2\r\n3,4\r\n'
    response._content = csv_bytes

    resp_data = client_with_url()._handle_response(response)
    assert isinstance(resp_data, bytes)
    assert csv_bytes == resp_data


def test_handle_response_jsonlines_response(client_with_url):
    expected = [{'key1': '1', 'key2': 2}, {'key3': '3', 'key4': 4}]
    response = Response()
    response.headers = {'Content-Type': 'application/jsonlines'}
    response.status_code = 200
    response._content = b'{"key1":"1","key2":2}\r\n{"key3":"3","key4":4}'
    assert client_with_url()._handle_response(response) == expected


def test_handle_response_html(client_with_url):
    expected = 'nice html response'
    response = Response()
    response.headers = {'Content-Type': 'text/html'}
    response.status_code = 200
    response._content = b'nice html response'
    assert client_with_url()._handle_response(response) == expected


def test_handle_response_html_no_content_type(client_with_url):
    expected = b'nice html response'
    response = Response()
    response.status_code = 200
    response._content = b'nice html response'
    assert client_with_url()._handle_response(response) == expected


def test_handle_response_json(client_with_url):
    expected = {'key1': '1', 'key2': 2}
    response = Response()
    response.headers = {'Content-Type': 'application/json'}
    response.status_code = 200
    response._content = b'{"key1":"1","key2":2}'
    assert client_with_url()._handle_response(response) == expected


def test_handle_response_json_204(client_with_url):
    response = Response()
    response.headers = {'Content-Type': 'application/json'}
    response.status_code = 204
    assert client_with_url()._handle_response(response) is None


def test_handle_response_json_no_content_type(client_with_url):
    expected = orjson.dumps({'key1': '1', 'key2': 2})
    response = Response()
    response.status_code = 200
    response._content = b'{"key1":"1","key2":2}'
    assert client_with_url()._handle_response(response) == expected


def test_handle_response_raise_for_status(client_with_url):
    response = Response()
    response.status_code = 400
    with pytest.raises(HTTPError):
        client_with_url()._handle_response(response)


def test_handle_response_raise_for_status_false(client_with_url):
    response = Response()
    response.status_code = 400
    assert client_with_url()._handle_response(response, raise_for_status=False) is None


def test_handle_response_txt(client_with_url):
    expected = 'foo bar'
    response = Response()
    response.headers = {'Content-Type': 'text/plain'}
    response.status_code = 200
    response._content = b'foo bar'
    assert client_with_url()._handle_response(response) == expected


def test_handle_response_txt_no_content_type(client_with_url):
    expected = b'foo bar'
    response = Response()
    response.status_code = 200
    response._content = b'foo bar'
    assert client_with_url()._handle_response(response) == expected


def test_handle_response_unknown_content_type(client_with_url):
    expected = b'foo bar'
    response = Response()
    response.headers = {'Content-Type': 'application/unknown'}
    response.status_code = 200
    response._content = b'foo bar'
    assert client_with_url()._handle_response(response) == expected


def test_handle_response_xml(client_with_url):
    expected = fromstring('<root><child name="child1">Content 1</child></root>')
    response = Response()
    response.headers = {'Content-Type': 'application/xml'}
    response.status_code = 200
    response._content = '<root><child name="child1">Content 1</child></root>'
    assert tostring(client_with_url()._handle_response(response)) == tostring(expected)


def test_handle_response_xml_no_content_type(client_with_url):
    expected = b'<root><child name="child1">Content 1</child></root>'
    response = Response()
    response.status_code = 200
    response._content = b'<root><child name="child1">Content 1</child></root>'
    assert client_with_url()._handle_response(response) == expected
