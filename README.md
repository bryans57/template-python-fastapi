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

**Note**: I put a .env-example that allow to connect to the docker database
(Section **DOCKER POSTGRESQL DB** below), if you don't want try it, you can
change the data for your own  (It's necessary for the project,
you'll get an error if you don't do it)

#### Suggested (Production)

```sh
uvicorn src.infrastructure.api.main:app --host 0.0.0.0 --port 8000
```

### Docker Postgresql DB

If you want to test the basic endpoint for get information, you can start or stop the docker container
to get info from the database

**(Remember that you need to have docker and docker-compose installed)**

```sh
## Start docker
make start-db

## Stop docker
make stop-db
```

#### Init Data for DB

You can find the file `init.sql` in the folder `sql-test-docker` that create the table and insert data,
with that data you can test the endpoint

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
../template-python-fastapi
├── Dockerfile
├── Makefile
├── README.md
├── azure-pipelines.yml
├── docker-compose.yml
├── env
│   └── azure.env
├── logs
│   └── app.log
├── manifests
│   ├── base
│   │   ├── deployment.yml
│   │   ├── hpa.yml
│   │   ├── kustomization.yml
│   │   ├── service.yml
│   │   └── virtual-service.yml
│   └── overlays
│       ├── dev
│       │   ├── hpa.yml
│       │   └── kustomization.yml
│       ├── prod
│       │   ├── hpa.yml
│       │   └── kustomization.yml
│       └── test
│           ├── hpa.yml
│           └── kustomization.yml
├── poetry.lock
├── precommit
│   └── validate_branch_name.sh
├── pyproject.toml
├── pytest.ini
├── sonar-project.properties
├── sql-test-docker
│   └── init.sql
├── src
│   ├── adapter
│   │   ├── controllers
│   │   │   └── person_controller.py
│   │   └── dtos
│   │       ├── person_dto.py
│   │       └── structure_response.py
│   ├── conf
│   │   └── containers.py
│   ├── domain
│   │   ├── exceptions
│   │   │   ├── errorcode.py
│   │   │   └── exceptions.py
│   │   ├── models
│   │   │   └── person.py
│   │   └── repositories
│   │       └── person_repository.py
│   ├── infrastructure
│   │   ├── api
│   │   │   ├── main.py
│   │   │   ├── middleware
│   │   │   │   ├── common_middleware.py
│   │   │   │   ├── error_middleware.py
│   │   │   │   └── verification_db.py
│   │   │   └── routers
│   │   │       ├── example_person_router.py
│   │   │       └── index.py
│   │   └── database
│   │       └── postgresql
│   │           ├── adapter
│   │           │   └── connection_config.py
│   │           ├── dao
│   │           │   └── person_dao.py
│   │           ├── postgresqldb.py
│   │           └── utils
│   │               └── db_utils.py
│   ├── usecases
│   │   └── person_info.py
│   └── util
│       ├── buffer.py
│       └── enviroments.py
└── tests
    ├── config
    │   ├── database
    │   │   └── dao
    │   │       ├── generic_dao_test.py
    │   │       └── person_dao_test.py
    │   └── mocks
    │       ├── informacion_db
    │       │   └── user_person_data_db.py
    │       └── tablas
    │           └── testdb.py
    ├── conftest.py
    └── infraestructure
        └── api
            └── person_test.py
```
