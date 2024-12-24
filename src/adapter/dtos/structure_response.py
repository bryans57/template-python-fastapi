from datetime import datetime
from typing import (
    Generic,
    Optional,
    TypeVar,
)

from pydantic import BaseModel


T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class Response(BaseModel, Generic[T]):
    isError: bool
    data: T
    timestamp: str


class StructureResponse:
    @staticmethod
    def ok(data: Optional[T] = None) -> Response[Optional[T]]:
        return Response(isError=False, data=data, timestamp=datetime.now().isoformat())

    @staticmethod
    def failure(exception: E) -> None:
        raise exception
