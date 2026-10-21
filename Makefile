PORT ?= 8000

# build-css идёт до migrate: alembic импортирует приложение,
# а оно на старте монтирует каталог static, который создаёт сборка стилей.
setup: install build-css migrate

install:
	uv sync
	npm ci

build-css:
	npm run build:css

dev:
	uv run fastapi dev page_analyzer/app.py --port $(PORT)

start:
	uv run fastapi run page_analyzer/app.py --port $(PORT) --workers 4

lint:
	uv run ruff check .

test:
	uv run pytest -vv

check: lint test

migrate:
	uv run alembic upgrade head

reset-db:
	uv run alembic downgrade base
	uv run alembic upgrade head

build:
	./build.sh

render-start:
	fastapi run page_analyzer/app.py --port $(PORT) --workers 5

.PHONY: setup install build-css dev start lint test check migrate reset-db \
	build render-start
