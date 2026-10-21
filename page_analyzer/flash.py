from typing import Literal

from fastapi import Request

FlashCategory = Literal["success", "danger", "info"]
SESSION_KEY = "flash_messages"


def add_flash(
    request: Request,
    text: str,
    category: FlashCategory = "info",
) -> None:
    messages = list(request.session.get(SESSION_KEY, []))
    messages.append({"category": category, "text": text})
    request.session[SESSION_KEY] = messages


def pop_flash_messages(request: Request) -> list[dict[str, str]]:
    return request.session.pop(SESSION_KEY, [])
