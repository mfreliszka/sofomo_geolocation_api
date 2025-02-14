

install:
	poetry install

run:
	uvicorn geolocation_api.main:application_factory --factory --reload

run-deploy:
	uvicorn --host 0.0.0.0 --port 8080 geolocation_api.main:application_factory --factory

lint:
	mypy .
	ruff check .
	ruff format --check .

format:
	ruff format .
