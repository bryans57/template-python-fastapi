# Template Python FastApi

## First Steps

It's necessary to install `poetry` first **(it's similar to npm)**

Link of installation: [poetry installation](https://python-poetry.org/docs/)

## Config Virtual Environment

**Execute:**

```sh
poetry shell
```

### Install libraries

* **install**: (when it's the first installation or something new), this means that there is no .lock

```sh
poetry install
```

* **lock**: (when we only want to update something)

```sh
poetry lock
```

### Config Pre-commit

**!Warning**: If you don't configure the pre-commit, it's possible that it doesn't deploy because of linter failures

```sh
pre-commit install
```

### Start Project

Recomended (Development)

```sh
fastapi dev src/infrastructure/api/main.py
```

Or where the main.py or the initial configuration of the project is located

Suggested (Production)

```sh
uvicorn src.infrastructure.api.main:app --host 0.0.0.0 --port 8000
```

## Testing

### Run test status

```sh
pytest -v
```

### Run test with logs (More detail)

```sh
pytest -s
```

#### Notes

## Project Structure

```text
project/
│
├── src/
│ ├── application/
│ │ └── use_case/
│ │ └── utils/
│ ├── domain/
│ │ └── dtos/
│ │ └── exceptions/
│ │ └── models/
│ │ └── repositories/
│ ├── infrastructure/
│ │ └── logging/
│ │ ├── persistence/
│ │ │ ├── database/
│ │ │ │ ├── dao/
│ │ │ │ └── database.py
│ │ └── web/
│ │ │ ├── api/
│ │ │ ├── apli_clients/
│ │ │ ├── controllers/
│ │ │ ├── http/
│ │ │ ├── flask_app.py
│ │ └── containers.py
│ └── main.py
│
└── tests/
├── application/
│ └── util/
│ └── test_simplified_address.py
├── infrastructure/
│ └── persistence/
│ └── database/
│ └── dao/
│ └── test_ciudad_dao.py
└── **init**.py
```
