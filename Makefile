.DEFAULT_GOAL = help


migration:  ## Make migration
	rye run alembic revision --autogenerate -m "$(ARGS)"

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
