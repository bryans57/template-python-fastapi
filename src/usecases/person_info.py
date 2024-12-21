from typing import List

from injector import inject

from src.adapter.dtos import PersonDto
from src.domain.models import Person
from src.infrastructure.database.postgresql.dao import PersonDAO


class PersonInfo:
    @inject
    def __init__(
        self,
        person_dao: PersonDAO,
    ):
        self.person_dao = person_dao

    def get_with_params(self, params: PersonDto) -> List[Person]:
        return self.person_dao.get_info(params.identifications, params.fieldsInfo)
