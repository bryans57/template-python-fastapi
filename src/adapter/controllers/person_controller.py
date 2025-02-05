from typing import (
    List,
    Optional,
    Union,
)

from injector import inject

from src.adapter.dtos import (
    PersonDto,
    PersonInsertDto,
)
from src.adapter.dtos.person_dto import (
    PersonDeleteDto,
    PersonUpdateDto,
)
from src.domain.models import Person
from src.infrastructure.database.postgresql.dao import PersonDAO
from src.usecases import PersonInfo


class PersonController:

    @inject
    def __init__(self, person_info: PersonInfo, person_dao: PersonDAO):
        self.person_info = person_info
        self.person_dao = person_dao

    def get_person(self, params: PersonDto) -> List[Person]:
        """
        You usually want to validate the data before sending it to the use case
        In this case we validate it when we receive it with our PersonDto
        """
        return self.person_info.get_with_params(params)

    def add_person(self, params: PersonInsertDto) -> Person:
        dump_params = params.model_dump()
        person = Person(**dump_params)
        return self.person_info.add(person)

    def update_person(self, params: PersonUpdateDto) -> Person:
        dump_params = params.model_dump()
        person = Person(**dump_params)
        return self.person_info.update(person)

    def delete_person(self, person_delete: PersonDeleteDto) -> Union[Optional[List[Person]], str]:
        elimated = self.person_dao.delete(person_delete.identifications)
        if elimated:
            return elimated
        return "No person was deleted"
