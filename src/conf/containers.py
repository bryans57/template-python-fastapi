from injector import (
    Injector,
    singleton,
)

from src.adapter.controllers.person_controller import PersonController
from src.domain.repositories.person_repository import PersonRepository
from src.infrastructure.database.postgresql.adapter.connection_config import (
    create_database_connection,
)
from src.infrastructure.database.postgresql.dao import PersonDAO
from src.infrastructure.database.postgresql.postgresql import Postgresql
from src.usecases import PersonInfo


class Container:
    def configure(self, binder):
        # Databases
        binder.bind(Postgresql, to=create_database_connection, scope=singleton)

        # Controllers
        binder.bind(PersonController, to=PersonController, scope=singleton)

        # Use Cases

        binder.bind(PersonInfo, to=PersonInfo, scope=singleton)

        # Repositories
        binder.bind(PersonRepository, to=PersonDAO, scope=singleton)


injector = Injector(Container().configure)
