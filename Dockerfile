FROM python:3.9-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as poetry

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.4.0

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN pip install "poetry==$POETRY_VERSION"
COPY . ./
RUN poetry install --no-dev -vvv

FROM base as final

ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
EXPOSE 8080
RUN chmod +x /app/docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]
