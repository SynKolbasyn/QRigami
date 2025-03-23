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
docker compose up --build
```

Optional flag `-d` to get free terminal after containers have started

```bash
docker compose up --build -d
```


# Development

## Dependencies

- [Docker](https://www.docker.com/)
- [uv](https://github.com/astral-sh/uv)

## Configuration

Configure project by setting variables in `.env`

```bash
cp ./template.env ./.env
```

## Develop

Install python

```bash
uv python install
```

Start database

```bash
docker compose up --build -d postgresql
```

Start Server

```bash
uv run ./qrigami/manage.py runserver
```
