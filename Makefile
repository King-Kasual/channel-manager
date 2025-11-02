SHELL := /bin/bash
.PHONY: format format-check lint check stop install clean build run psql-run run-all \
        install-deps revision upgrade downgrade current history \
        run-migrations docker-migrate

ALEMBIC := alembic
PY := python3
PIP := pip3

format:
	python3 -m black .

format-check:
	python3 -m black --check .

lint:
	python3 -m pylint $(shell git ls-files '*.py' ':(exclude)alembic/**')

check: format-check lint

stop:
	docker compose down

install:
	pip3 install -r requirements.txt

# Install dependencies (alias)
install-deps: install

clean:
	docker image prune -a

build:
	docker compose build app

run:
	docker compose down app
	docker compose up app -d --build

psql-run:
	docker compose up postgres

run-all:
	docker compose up -d

# -----------------------
# Migration helpers
# -----------------------

# Create a new alembic revision with autogenerate
# Usage: make revision MSG="add new table"
revision:
ifndef MSG
	$(error MSG is required, e.g. make revision MSG="add foo")
endif
ifeq ($(strip $(REVID)),)
	$(error REVID is required, e.g. make revision REVID="0001")
endif
	$(ALEMBIC) revision --autogenerate --rev-id $(REVID) -m "$(MSG)"

upgrade:
	$(ALEMBIC) upgrade head

downgrade:
ifndef REV
	$(error REV is required, e.g. make downgrade REV=base)
endif
	$(ALEMBIC) downgrade $(REV)

current:
	$(ALEMBIC) current

history:
	$(ALEMBIC) history --verbose

run-migrations:
	$(PY) scripts/run_migrations.py

# Run migrations inside the app container (useful in CI or when using compose)
docker-migrate:
	docker compose run --rm app python scripts/run_migrations.py
