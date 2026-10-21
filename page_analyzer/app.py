from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Any

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from page_analyzer import repository
from page_analyzer.checker import check_url
from page_analyzer.config import get_settings
from page_analyzer.db import SessionDep, engine
from page_analyzer.flash import add_flash, pop_flash_messages
from page_analyzer.models import Url
from page_analyzer.url_validator import normalize_url, validate_url

BASE_DIR = Path(__file__).parent


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    SessionMiddleware,
    secret_key=get_settings().secret_key.get_secret_value(),
)
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")


def render(
    request: Request,
    name: str,
    context: dict[str, Any] | None = None,
    status_code: int = 200,
) -> Response:
    page_context = {
        "flash_messages": pop_flash_messages(request),
        **(context or {}),
    }
    return templates.TemplateResponse(
        request,
        name,
        page_context,
        status_code=status_code,
    )


def redirect_to_url(request: Request, url_id: int) -> RedirectResponse:
    return RedirectResponse(
        request.url_for("url_show", id=url_id),
        status_code=303,
    )


async def get_url_or_404(session: SessionDep, url_id: int) -> Url:
    url = await repository.get_url(session, url_id)
    if url is None:
        raise HTTPException(status_code=404)
    return url


@app.get("/", name="index", response_class=HTMLResponse)
async def index(request: Request) -> Response:
    return render(request, "index.html")


@app.get("/urls", name="urls_index", response_class=HTMLResponse)
async def urls_index(request: Request, session: SessionDep) -> Response:
    urls = await repository.get_urls_with_last_check(session)
    return render(request, "urls/index.html", {"urls": urls})


@app.post("/urls", name="urls_create")
async def urls_create(
    request: Request,
    session: SessionDep,
    url: Annotated[str, Form()] = "",
) -> Response:
    address = url.strip()
    error = validate_url(address)
    if error:
        add_flash(request, error, "danger")
        return render(
            request,
            "index.html",
            {"url_name": address},
            status_code=422,
        )

    name = normalize_url(address)
    existing_url = await repository.find_url_by_name(session, name)
    if existing_url is not None:
        add_flash(request, "Страница уже существует", "info")
        return redirect_to_url(request, existing_url.id)

    new_url = Url(name=name)
    await repository.save(session, new_url)
    add_flash(request, "Страница успешно добавлена", "success")
    return redirect_to_url(request, new_url.id)


@app.get("/urls/{id}", name="url_show", response_class=HTMLResponse)
async def url_show(request: Request, id: int, session: SessionDep) -> Response:
    url = await get_url_or_404(session, id)
    return render(request, "urls/show.html", {"url": url})


@app.post("/urls/{id}/checks", name="url_checks_create")
async def url_checks_create(
    request: Request,
    id: int,
    session: SessionDep,
) -> Response:
    url = await get_url_or_404(session, id)
    url_check = await check_url(url.id, url.name)
    if url_check is None:
        add_flash(request, "Произошла ошибка при проверке", "danger")
        return redirect_to_url(request, url.id)

    await repository.save(session, url_check)
    add_flash(request, "Страница успешно проверена", "success")
    return redirect_to_url(request, url.id)


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> Response:
    if exc.status_code == 404:
        return render(request, "errors/404.html", status_code=404)
    return render(request, "errors/500.html", status_code=exc.status_code)


@app.exception_handler(Exception)
async def server_error_handler(request: Request, exc: Exception) -> Response:
    return render(request, "errors/500.html", status_code=500)
