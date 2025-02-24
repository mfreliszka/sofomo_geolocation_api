#FROM python:3.11-slim
# docker image with poetry 1.8.5 and python 3.11.11 preinstalled
FROM pfeiffermax/python-poetry:1.14.0-poetry1.8.5-python3.11.11-slim-bookworm

# Install dependencies for building the app
RUN apt-get update && apt-get install -y make

WORKDIR /src

COPY poetry.lock pyproject.toml /src/
COPY Makefile /src/

# Install poetry
# RUN curl -sSL https://install.python-poetry.org | python3 - \
#     && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Install dependencies
RUN make install-deploy

# Copy app directory into src
COPY . /src/

EXPOSE 8080

CMD ["make", "run-deploy"]
