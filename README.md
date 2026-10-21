# Анализатор страниц на FastAPI

[![hexlet-check](https://github.com/kicha3007-boop/fastapi-project-317/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kicha3007-boop/fastapi-project-317/actions)
[![Python CI](https://github.com/kicha3007-boop/fastapi-project-317/actions/workflows/pyci.yml/badge.svg)](https://github.com/kicha3007-boop/fastapi-project-317/actions/workflows/pyci.yml)

Page Analyzer — сайт, который проверяет страницы на SEO-пригодность: пользователь добавляет адрес,
запускает проверку и видит код ответа, `h1`, `title` и `description` страницы.

Учебный проект Хекслета: https://ru.hexlet.io/programs/fastapi
Как это должно работать: https://files.hexlet.app/a/vfyo3a

Деплой на render.com пока не выполнен — ссылка на приложение появится здесь.

## Стек

Python 3.14, FastAPI, SQLModel (асинхронная сессия, asyncpg), Alembic, PostgreSQL, Jinja2,
httpx, BeautifulSoup, Tailwind CSS, uv, ruff, pytest.

## Требования

- Python 3.14 и [uv](https://docs.astral.sh/uv/)
- Node.js и npm — только для сборки стилей
- PostgreSQL

## Установка и запуск

```bash
git clone https://github.com/kicha3007-boop/fastapi-project-317.git
cd fastapi-project-317
cp .env.example .env     # заполнить DATABASE_URL и SECRET_KEY
make setup               # uv sync, npm ci, сборка CSS, миграции (uv run alembic upgrade head)
make dev                 # uv run fastapi dev — режим разработки с перезапуском, http://localhost:8000
make start               # uv run fastapi run --workers 4 — без слежения за файлами
```

Переменные окружения:

- `DATABASE_URL` — строка подключения, например `postgres://user:password@localhost:5432/page_analyzer`
  (драйвер `asyncpg` подставляется автоматически)
- `SECRET_KEY` — ключ подписи сессии для flash-сообщений

## Разработка

```bash
uv run ruff check .      # make lint
uv run pytest -vv        # make test
make check               # линтер и тесты
make migrate             # накатить миграции
make build-css           # пересобрать стили после правки шаблонов
```

Новая миграция по изменённым моделям: `uv run alembic revision --autogenerate -m "описание"`.

Деплой на render.com: команда сборки `make build` (скрипт `build.sh`), запуска — `make render-start`,
переменные `DATABASE_URL` и `SECRET_KEY`.

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
