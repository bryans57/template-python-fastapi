from typing import List

from injector import inject

from src.adapter.dtos import PersonDto
from src.domain.models import Person
from src.usecases import PersonInfo


class PersonController:

    @inject
    def __init__(self, person_info: PersonInfo):
        self.person_info = person_info

    def validate_person(self, params: PersonDto) -> List[Person]:
        """
        You usually want to validate the data before sending it to the use case
        In this case we validate it when we receive it with our PersonDto
        """
        return self.person_info.get_with_params(params)
