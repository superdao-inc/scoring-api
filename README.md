# Scoring API

## Description
REST API for our scroring platform. Used to get wallets data (including calculated superrank score)
grouped by labels `audience/`, some claimed contracts `claimed/` and so on.


For futher details see swagger docs at `/docs/`

## Requirements

- [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
- python 3.9


## Dev Setup
```bash
$ cp .env.example .env
$ docker-compose up -d
```

## Commands
```bash
# list all available commands
make help

# install packages with dev dependencies
make install

# run linter
make lint

# make formatter
make format

# run tests
make tests

# run all migrations
make migrate

# run app in development mode
make watch
```

## Environment variables
| name        | description                  | default value |
| ----------- | ---------------------------- | ------------- |
| MODE        | application mode             | dev           |
| DB_NAME     | PostgreSQL database name     | scoring_api   |
| DB_HOST     | PostgreSQL database host     | localhost     |
| DB_PORT     | PostgreSQL database port     | 5432          |
| DB_USER     | PostgreSQL database user     | postgres      |
| DB_PASSWORD | PostgreSQL database password | postgres      |
| SENTRY_DSN  | Sentry DSN                   |               |