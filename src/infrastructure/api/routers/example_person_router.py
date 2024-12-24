from typing import List

from fastapi import (
    APIRouter,
    Depends,
)

from src.adapter.controllers import PersonController
from src.adapter.dtos import (
    PersonDto,
    PersonInsertDto,
    Response,
    StructureResponse,
)
from src.conf import injector
from src.domain.models.person import Person


basic_person_example_route = APIRouter(prefix="/example-people")


# We use a post method because we are going to send a body
@basic_person_example_route.post(
    "/info",
    response_model=Response[List[Person]],
    tags=["Example Router Postgresql"],
    description="""Let you get information from a dump table
    Note: The input fields are the same as the output""",
    response_model_exclude_none=True,
)
async def start(
    body: PersonDto,
    server: PersonController = Depends(lambda: injector.get(PersonController)),
):
    data = server.get_person(body)
    return StructureResponse.ok(data)


@basic_person_example_route.post(
    "/add",
    tags=["Example Router Postgresql"],
    description="""Let you add a person to the dump table""",
    response_model=Response[Person],
    response_model_exclude_none=True,
)
async def add_person(
    body: PersonInsertDto,
    server: PersonController = Depends(lambda: injector.get(PersonController)),
):
    data = server.add_person(body)
    return StructureResponse.ok(data)
