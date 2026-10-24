import re

from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=15,
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):

        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*?.]).*$"

        if not re.fullmatch(pattern, password):
            raise ValueError("Password is not valid")
        return password


class UserLogin(BaseModel):
    email: EmailStr
    password: str
