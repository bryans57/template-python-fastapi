from pydantic import (
    BaseModel,
    Field,
    constr,
    field_validator,
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
