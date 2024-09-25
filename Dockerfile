FROM python:3.10.15-alpine3.20

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.3 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # Project paths
    VENV_PATH="/opt/app/.venv" \
    APP_PATH="/opt/app" \
    # Development dependencies
    DEV_DEPENDENCIES="bash vim curl" \
    # Project variables
    FLASK_ENV=development \
    DJANGO_DEBUG=False \
    PROJECT_NAME=USER-TRANSACTIONS

USER root
RUN apt-get update; \
    apt-get install -y --no-install-recommends $DEV_DEPENDENCIES; \
    curl -o /tmp/get-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py; \
    python /tmp/get-poetry.py; \
    rm /tmp/get-poetry.py; \
    mkdir -p "$APP_PATH"; \
    apt-get clean;

# Configure Poetry
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Configure project data
COPY . /opt/app
WORKDIR /opt/app
RUN poetry install --no-dev  && rm -rf ~/.cache/pypoetry/{cache,artifacts}
  
ENTRYPOINT ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]