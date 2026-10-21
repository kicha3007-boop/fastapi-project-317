from urllib.parse import urlparse

from pydantic import HttpUrl, TypeAdapter, ValidationError

MAX_URL_LENGTH = 255

URL_REQUIRED = "URL обязателен"
URL_TOO_LONG = "URL превышает 255 символов"
URL_INVALID = "Некорректный URL"

http_url = TypeAdapter(HttpUrl)


def validate_url(url: str) -> str | None:
    """Вернуть текст ошибки или None, если адрес корректен."""
    if not url:
        return URL_REQUIRED
    if len(url) > MAX_URL_LENGTH:
        return URL_TOO_LONG
    try:
        http_url.validate_python(url)
    except ValidationError:
        return URL_INVALID
    return None


def normalize_url(url: str) -> str:
    parts = urlparse(url)
    return f"{parts.scheme.lower()}://{parts.netloc.lower()}"
