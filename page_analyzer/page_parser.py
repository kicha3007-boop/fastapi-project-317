from bs4 import BeautifulSoup, Tag

MAX_FIELD_LENGTH = 255


def get_text(tag: Tag | None) -> str:
    return tag.get_text(strip=True) if tag else ""


def parse_page(html: str) -> dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    description = soup.find("meta", attrs={"name": "description"})
    content = description.get("content", "") if description else ""
    seo = {
        "h1": get_text(soup.h1),
        "title": get_text(soup.title),
        "description": str(content).strip(),
    }
    return {key: value[:MAX_FIELD_LENGTH] for key, value in seo.items()}
