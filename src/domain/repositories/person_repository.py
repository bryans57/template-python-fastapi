from abc import (
    ABC,
    abstractmethod,
)
from typing import List

from src.domain.models import Person


class PersonRepository(ABC):
    @abstractmethod
    def get_info(self, identifications: list, fields_info: list) -> List[Person]:
        pass
