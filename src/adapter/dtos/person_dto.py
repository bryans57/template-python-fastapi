from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


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
