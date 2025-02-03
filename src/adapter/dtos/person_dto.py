from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    constr,
    field_validator,
    model_validator,
)

from src.domain.models import Person


allow_fields = {
    "identification",
    "first_name",
    "last_name",
    "weight",
    "height",
    "age",
    "city",
    "country",
    "email",
    "phone",
    "address",
}


class PersonDto(BaseModel):
    identifications: list[str] = Field(
        ..., min_length=1, description="If the identification is not provided, the response will be an empty list"
    )
    fieldsInfo: list[str]

    @field_validator("fieldsInfo", mode="before")
    @classmethod
    def check_fields_info(cls, v):
        if not isinstance(v, list):
            raise TypeError("fieldsInfo must be a list")
        invalid_fields = [field for field in v if field not in allow_fields]
        if invalid_fields:
            raise ValueError(f"Invalid fields: {invalid_fields}. Only allow the next fields: {allow_fields}")
        return v


class PersonInsertDto(Person):
    identification: str = Field(
        ..., pattern=r"^\d+$", min_length=6, max_length=15, description="Numeric ID between 6-15 characters"
    )
    first_name: constr(min_length=1, max_length=50) = Field(..., description="The person's first name")
    last_name: constr(min_length=1, max_length=50) = Field(..., description="The person's last name")
    age: int = Field(..., gt=0, lt=120, description="The person's age (between 1 and 119)")
    city: constr(min_length=1, max_length=100) = Field(..., description="The person's city of residence")
    country: constr(min_length=1, max_length=100) = Field(..., description="The person's country of residence")
    phone: constr(pattern=r"^\+?\d{7,15}$") = Field(
        ..., description="Phone number in international format, e.g., +123456789"
    )
    address: constr(min_length=5, max_length=200) = Field(..., description="The person's address")


class PersonUpdateDto(BaseModel):
    identification: str = Field(
        ..., pattern=r"^\d+$", min_length=6, max_length=15, description="Numeric ID between 6-15 characters"
    )
    first_name: Optional[constr(min_length=1, max_length=50)] = Field(None, description="The person's first name")
    last_name: Optional[constr(min_length=1, max_length=50)] = Field(None, description="The person's last name")
    age: Optional[int] = Field(None, gt=0, lt=120, description="The person's age (between 1 and 119)")
    city: Optional[constr(min_length=1, max_length=100)] = Field(None, description="The person's city of residence")
    country: Optional[constr(min_length=1, max_length=100)] = Field(
        None, description="The person's country of residence"
    )
    phone: Optional[constr(pattern=r"^\+?\d{7,15}$")] = Field(
        None, description="Phone number in international format, e.g., +123456789"
    )
    address: Optional[constr(min_length=5, max_length=200)] = Field(None, description="The person's address")
    weight: Optional[float] = Field(None, description="The person's weight")
    height: Optional[float] = Field(None, description="The person's height")
    email: Optional[constr(min_length=5, max_length=200)] = Field(None, description="The person's email")

    @field_validator("email")
    @classmethod
    def check_email(cls, v):
        if v is not None and "@" not in v:
            raise ValueError("Invalid email")
        return v

    @model_validator(mode="before")
    @classmethod
    def check_at_least_one_field(cls, values):
        """Ensure that at least one field besides 'identification' is provided."""
        if not isinstance(values, dict):
            raise ValueError("Invalid data format")  # Extra safety check

        # Filter out 'identification' and check if at least one other field is provided
        extra_fields = {k: v for k, v in values.items() if k != "identification" and v is not None}
        if len(extra_fields) == 0:
            raise ValueError("At least one field besides 'identification' must be provided")

        return values
