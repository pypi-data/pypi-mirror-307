from fitrequest.client import FitRequest


def test_is_url_valid_https():
    assert FitRequest._is_url_valid(url='https://www.skillcorner.com')


def test_is_url_valid_http():
    assert FitRequest._is_url_valid(url='http://www.skillcorner.com')


def test_is_url_valid_no_subdomain():
    assert FitRequest._is_url_valid(url='https://skillcorner.com')


def test_is_url_valid_no_top_level_domain():
    assert FitRequest._is_url_valid(url='https://www.skillcorner')


def test_is_url_valid_no_subdomain_and_top_level_domain():
    assert FitRequest._is_url_valid(url='https://skillcorner')


def test_is_url_valid_invalid_scheme_missing_slash():
    assert FitRequest._is_url_valid(url='https:/skillcorner.com') is False


def test_is_url_valid_invalid_scheme_missing_colon():
    assert FitRequest._is_url_valid(url='https//skillcorner.com') is False


def test_is_url_valid_invalid_scheme_one_more_slash():
    assert FitRequest._is_url_valid(url='https:///skillcorner.com') is False


def test_is_url_valid_no_scheme():
    assert FitRequest._is_url_valid(url='www.skillcorner.com') is False


def test_is_url_valid_wrong_type_int():
    assert FitRequest._is_url_valid(url=155) is False


def test_is_url_valid_wrong_type_list():
    assert FitRequest._is_url_valid(url=['https://skillcorner.com']) is False


def test_is_url_valid_None():
    assert FitRequest._is_url_valid(url=None) is False
