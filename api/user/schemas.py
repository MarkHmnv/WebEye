from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(20)]


class LoginUser(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(20)]


class UserProfile(BaseModel):
    name: str
    email: str


class UpdateUserPartial(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(20)] | None = None
    email: EmailStr | None = None