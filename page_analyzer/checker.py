import logging

import httpx

from page_analyzer.models import UrlCheck
from page_analyzer.page_parser import parse_page

REQUEST_TIMEOUT = 10

logger = logging.getLogger(__name__)


async def check_url(url_id: int, address: str) -> UrlCheck | None:
    """Запросить сайт и собрать проверку; None, если ответ не 2xx."""
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=REQUEST_TIMEOUT,
        ) as client:
            response = await client.get(address)
            response.raise_for_status()
    except httpx.HTTPError as error:
        logger.warning("Check of %s failed: %s", address, error)
        return None

    return UrlCheck(
        url_id=url_id,
        status_code=response.status_code,
        **parse_page(response.text),
    )
