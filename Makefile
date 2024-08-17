.DEFAULT_GOAL = help

install:  ## Install dependencies
	rye sync

serve:  ## Run server locally
	rye run uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

migration:  ## Make migration
	rye run alembic revision --autogenerate -m "$(ARGS)"

migrate:  ## Apply migrations
	rye run alembic upgrade head

lint:  ## Check lint
	rye run lint

test:  ## Check tests
	rye test

coverage:  ## Check test coverage
	rye run python -m pytest --cov=app

coverage-report:  ## Make test coverage report
	rye run python -m pytest --cov=app --cov-report xml

type:  ## Run type check
	rye run mypy app

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
