.PHONY: install migrate run test shell db-up db-down docker-up docker-down docker-build

install:
	uv sync

db-up:
	docker compose up -d db

db-down:
	docker compose down

migrate:
	uv run python manage.py migrate

run:
	uv run python manage.py runserver

test:
	uv run pytest

shell:
	uv run python manage.py shell

superuser:
	uv run python manage.py createsuperuser

# Docker commands
docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-migrate:
	docker compose exec web uv run python manage.py migrate

docker-test:
	docker compose exec web uv run pytest