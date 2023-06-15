.DEFAULT_GOAL = help

install:  ## Install dependencies
	poetry install

serve:  ## Run server locally
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

migration:  ## Make migration
	poetry run alembic revision --autogenerate -m "$(ARGS)"

migrate:  ## Apply migrations
	poetry run alembic upgrade head

lint:  ## Check lint
	poetry run flake8 app

test:  ## Check tests
	poetry run python -m pytest

coverage:  ## Check test coverage
	poetry run python -m pytest --cov=app

coverage-report:  ## Make test coverage report
	poetry run python -m pytest --cov=app --cov-report xml

type:  ## Run type check
	poetry run mypy app

run: .env  ## Run app in docker compose
	docker-compose up

down:  ## Stop app in docker compose
	docker-compose down

check: lint coverage-report type  ## Complex check (linter and tests)

.env:  ## Create env file from example
	test ! -f .env && cp .env.example .env

help:  ## Display help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'
