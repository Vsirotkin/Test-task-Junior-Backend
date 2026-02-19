.PHONY: install migrate run test shell

install:
	uv sync

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