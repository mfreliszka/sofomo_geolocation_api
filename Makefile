install:
	poetry install

install-deploy:
	poetry config virtualenvs.create false
	poetry install

run:
	uvicorn app.main:application_factory --factory --reload

run-deploy:
	uvicorn --host 0.0.0.0 --port 8080 app.main:application_factory --factory

lint:
	ruff check app tests config
	ruff format --check app tests config

format:
	ruff format .

migrate:
	poetry run alembic upgrade head

makemigrations:
	poetry run alembic revision --autogenerate -m "New Migration"
