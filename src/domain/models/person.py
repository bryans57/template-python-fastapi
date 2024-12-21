from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
    identification: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    weight: Optional[Decimal] = None
    height: Optional[Decimal] = None
    age: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
