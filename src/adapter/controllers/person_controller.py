from typing import List

from injector import inject

from src.adapter.dtos import (
    PersonDto,
    PersonInsertDto,
)
from src.adapter.dtos.person_dto import PersonUpdateDto
from src.domain.models import Person
from src.usecases import PersonInfo


class PersonController:

    @inject
    def __init__(self, person_info: PersonInfo):
        self.person_info = person_info

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

    def uptade_person(self, params: PersonUpdateDto) -> Person:
        dump_params = params.model_dump()
        person = Person(**dump_params)
        return self.person_info.update(person)
