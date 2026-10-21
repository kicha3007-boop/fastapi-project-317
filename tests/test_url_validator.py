import pytest

from page_analyzer.url_validator import (
    URL_INVALID,
    URL_REQUIRED,
    URL_TOO_LONG,
    normalize_url,
    validate_url,
)


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("http://example.test/blog/", "http://example.test"),
        ("http://example.test/users/1", "http://example.test"),
        ("HTTPS://EXAMPLE.test/Path?q=1", "https://example.test"),
        ("http://localhost:8000/page", "http://localhost:8000"),
    ],
)
def test_normalize_url_keeps_scheme_and_host(given, expected):
    assert normalize_url(given) == expected


@pytest.mark.parametrize(
    "url",
    ["http://example.test/blog/", "https://ru.hexlet.io", "http://wrong.test"],
)
def test_validate_url_accepts_valid_url(url):
    assert validate_url(url) is None


@pytest.mark.parametrize(
    ("given", "message"),
    [
        ("", URL_REQUIRED),
        ("httpsss://abcabca@test.ru", URL_INVALID),
        ("not a url", URL_INVALID),
        ("http://example.test/" + "a" * 255, URL_TOO_LONG),
    ],
)
def test_validate_url_rejects_invalid_url(given, message):
    assert validate_url(given) == message
