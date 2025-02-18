FROM python:3.11

# Install dependencies for building the app
RUN apt update && \
    apt install make gcc g++ -y && \
    pip install --no-cache-dir poetry

WORKDIR /src/

# Copy necessary files to /src/ folder
COPY poetry.lock pyproject.toml /src/
COPY Makefile /src/

# Install dependencies and deploy
RUN make install-deploy

# Install the project dependencies with poetry
RUN pip install poetry && poetry install --no-root

# Copy the remaining files, including README.md
COPY . /src/

EXPOSE 8000

CMD ["make", "run"]
