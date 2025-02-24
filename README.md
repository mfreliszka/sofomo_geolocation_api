# Sofomo Geolocation API

A FastAPI-based application that provides CRUD operations for geolocation data, including a database health-check middleware for production environments. This project uses SQLAlchemy, Alembic for migrations, and Poetry for dependency management.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)
- [Database Migrations](#database-migrations)
- [Testing](#testing)
- [Docker Usage](#docker-usage)
- [Makefile Commands](#makefile-commands)

## Features
- FastAPI endpoints for creating, retrieving, updating, and deleting geolocation records in the database
- Maintenance endpoint for quick health checks (e.g., ping)
- Alembic migrations for database schema changes
- Middleware that checks database availability (only active in non-testing environments)
- In-memory SQLite testing, ensuring test isolation
- Docker Compose support for easy containerized deployment
- Poetry for dependency management

## Requirements
- Poetry (for Python dependency management)
- Docker (to run Dockerized environments, optional)
- Docker Compose (for building and orchestrating containers)

*(Alternatively, you can install and run everything directly on your machine, but Docker usage is recommended for production-like environments.)*

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/yourprojectname.git
cd yourprojectname
```

2. Install dependencies using Poetry:
```bash
make install
```
This will create a virtual environment (if not disabled) and install all Python dependencies.

3. Configure environment variables as needed. For local development, you might have a `.env` file with database credentials or other configs.

## Running the Application

There are two primary ways:

### 1. Local (using uvicorn)
```bash
make run
```
- This calls `uvicorn app.main:application_factory --factory --reload`, which automatically restarts on code changes
- By default, the app will listen on `http://127.0.0.1:8000`

### 2. Docker Compose
```bash
make up
```
- Builds and starts the containers (including your FastAPI app and any other services)
- By default, the FastAPI app will listen on port 8080 inside the container (depending on your Docker config)

## Endpoints

Below is a summary of available endpoints. The base prefix `/api` may vary if you have set it differently.

### Maintenance

#### Ping
- `GET /api/maintenance/ping`
- Returns a simple health-check response

### Geolocation

#### Get Geolocation From Database
- `GET /api/geolocation`
- Query parameters: `ip_address` (required)

#### Add Geolocation To Database
- `POST /api/geolocation`
- Body example:
```json
{
  "ip_address": "8.8.8.8"
}
```

#### Delete Geolocation From Database
- `DELETE /api/geolocation`
- Query parameters: `ip_address` (required)

#### List All Geolocations From Database
- `GET /api/geolocation/list`
- Returns a list of all geolocation records

## Database Migrations

We use Alembic for handling migrations:

1. Create a new migration (autogenerate changes):
```bash
make makemigrations
```
This will create a new migration file in your `migrations/versions` folder.

2. Apply migrations (upgrade to latest):
```bash
make migrate
```

## Testing

We rely on Pytest with pytest-asyncio. By default, the tests run against an in-memory SQLite database. To run the test suite:

```bash
make test
```

This command sets `TESTING=1` and uses Docker Compose to run the backend service, executing `pytest . -vv`.

If you want to run tests locally without Docker, you can do:
```bash
TESTING=1 pytest -vv
```
*(assuming you have the correct environment set up)*

## Docker Usage

```bash
# Build containers
make build

# Start containers
make up

# Stop & remove containers
make down
```

## Makefile Commands

Below is a summary of the available make targets in the Makefile:

| Command | Description |
|---------|-------------|
| `make install` | Install Python dependencies via Poetry (creates a virtualenv by default) |
| `make install-deploy` | Poetry install with virtualenvs.create false (for containerized environments) |
| `make run` | Run the FastAPI app locally with autoreload |
| `make run-deploy` | Run the FastAPI app in a production-like manner (no reload) |
| `make lint` | Lint code with ruff |
| `make format` | Auto-format code with ruff's format command |
| `make migrate` | Apply alembic migrations (upgrade head) |
| `make makemigrations` | Generate a new Alembic migration |
| `make up` | Start the Docker Compose services |
| `make down` | Stop and remove Docker Compose services |
| `make build` | Build the Docker Compose images |
| `make test` | Run the test suite in Docker with TESTING=1 |