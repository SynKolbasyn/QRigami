# Deploy

## Dependencies

- [Docker](https://www.docker.com/)

## Configuration

Configure project by setting variables in `.env`

```bash
cp ./template.env ./.env
```

## Run

```bash
docker compose up
```

Optional flag `-d` to get free terminal after containers have started

```bash
docker compose up -d
```

[Click](https://localhost/)


# Development

## Dependencies

- [uv](https://github.com/astral-sh/uv)

## Configuration and debugging

Install python

```bash
uv python install
```

Run migrations

```bash
DJANGO_DEBUG=True uv run ./qrigami/manage.py migrate
```

Start server

```bash
DJANGO_DEBUG=True uv run ./qrigami/manage.py runserver
```

[Click](http://localhost:8000/)
