

install:
	poetry install

install-deploy:
	poetry config virtualenvs.create false
	poetry install

run:
	uvicorn geolocation_api.main:application_factory --factory --reload

run-deploy:
	uvicorn --host 0.0.0.0 --port 8080 geolocation_api.main:application_factory --factory

lint:
	mypy geolocation_api config
	ruff check geolocation_api tests config
	ruff format --check geolocation_api tests config

format:
	ruff format .

migrate:
	poetry run alembic upgrade head

makemigrations:
	poetry run alembic revision --autogenerate -m "New Migration"

dropdb:
	poetry run alembic downgrade base

createdb:
	poetry run alembic init alembic
