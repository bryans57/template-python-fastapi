from fastapi import APIRouter

from src.infrastructure.api.routers.example_person_router import (
    basic_person_example_route,
)


routes = APIRouter()

routes.include_router(basic_person_example_route)
