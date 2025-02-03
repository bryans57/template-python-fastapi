from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
)

from src.domain.models import Person


class PersonRepository(ABC):
    @abstractmethod
    def get_info(self, identifications: list, fields_info: list) -> List[Person]:
        pass

    def add(self, person: Person) -> Person:
        pass

    def update(self, person: Person) -> Person:
        pass

    def delete(self, identifications: List[str]) -> Optional[List[Person]]:
        pass
