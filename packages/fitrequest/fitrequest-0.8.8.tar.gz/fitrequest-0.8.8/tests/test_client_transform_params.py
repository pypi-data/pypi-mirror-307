import pytest

from fitrequest.client import FitRequest


def test_transform_params_with_list_int():
    params = {'arg1': 'value1', 'arg2': [2, 3, 4, 5]}
    expected = {'arg1': 'value1', 'arg2': '2,3,4,5'}
    value = FitRequest._transform_params(params=params)
    assert value == expected


def test_transform_params_with_list_int_and_str():
    params = {'arg1': ['value1', 'foo', 'bar'], 'arg2': [2, 3, 4, 5], 'arg3': 10}
    expected = {'arg1': 'value1,foo,bar', 'arg2': '2,3,4,5', 'arg3': 10}
    value = FitRequest._transform_params(params=params)
    assert value == expected


def test_transform_params_with_list_and_set():
    params = {'arg1': ['value1', 'foo', 'bar'], 'arg2': {2, 3, 4, 5}, 'arg3': 10}
    expected = {'arg1': 'value1,foo,bar', 'arg2': '2,3,4,5', 'arg3': 10}
    value = FitRequest._transform_params(params=params)
    assert value['arg1'] == expected['arg1']
    assert sorted(value['arg2'].split(',')) == sorted(expected['arg2'].split(','))


def test_transform_params_with_set_int():
    params = {'arg1': 'value1', 'arg2': {2, 3, 4, 5}}
    expected = {'arg1': 'value1', 'arg2': '2,3,4,5'}
    value = FitRequest._transform_params(params=params)
    assert sorted(value['arg1'].split(',')) == sorted(expected['arg1'].split(','))
    assert sorted(value['arg2'].split(',')) == sorted(expected['arg2'].split(','))


def test_transform_params_with_set_int_and_str():
    params = {'arg1': {'value1', 'foo', 'bar'}, 'arg2': {2, 3, 4, 5}, 'arg3': 10}
    expected = {'arg1': 'value1,foo,bar', 'arg2': '2,3,4,5', 'arg3': 10}
    value = FitRequest._transform_params(params=params)
    assert sorted(value['arg1'].split(',')) == sorted(expected['arg1'].split(','))
    assert sorted(value['arg2'].split(',')) == sorted(expected['arg2'].split(','))


def test_transform_params_no_changes():
    params = {'arg1': 'value1', 'arg2': 'value2'}
    expected = {'arg1': 'value1', 'arg2': 'value2'}
    value = FitRequest._transform_params(params=params)
    assert value == expected


def test_transform_params_no_changes_with_list_as_str():
    params = {'arg1': 'value1', 'arg2': 'value2,value3,value4'}
    expected = {'arg1': 'value1', 'arg2': 'value2,value3,value4'}
    value = FitRequest._transform_params(params=params)
    assert value == expected


def test_transform_params_empty():
    value = FitRequest._transform_params(params={})
    assert not value


def test_transform_params_invalid_type_list():
    with pytest.raises(AttributeError):
        FitRequest._transform_params(params=[1, 2, 3])


def test_transform_params_invalid_type_str():
    with pytest.raises(AttributeError):
        FitRequest._transform_params(params='test')
