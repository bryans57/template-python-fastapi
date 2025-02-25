from injector import (
    Injector,
    NoScope,
    singleton,
)

from src.adapter.controllers.person_controller import PersonController
from src.domain.repositories.person_repository import PersonRepository
from src.infrastructure.database.postgresql.adapter.connection_config import (
    create_database_connection,
)
from src.infrastructure.database.postgresql.dao import PersonDAO
from src.infrastructure.database.postgresql.postgresqldb import PostgresqlDB
from src.usecases import PersonInfo
from src.util import Enviroments


class Container:
    def configure(self, binder):
        # Databases
        binder.bind(PostgresqlDB, to=create_database_connection, scope=singleton)

        # Scope for pytest - don't move if don't understand too much
        scope_defined = NoScope if Enviroments.PYTEST else singleton

        # Controllers
        binder.bind(PersonController, to=PersonController, scope=scope_defined)

        # Use Cases

        binder.bind(PersonInfo, to=PersonInfo, scope=scope_defined)

        # Repositories

        binder.bind(PersonRepository, to=PersonDAO, scope=scope_defined)


injector = Injector(Container().configure)
