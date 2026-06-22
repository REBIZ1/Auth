from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

NameStr = Annotated[str, Field(min_length=1, max_length=150)]
PasswordStr = Annotated[str, Field(min_length=8, max_length=200)]


class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: NameStr
    middle_name: NameStr | None = None
    last_name: NameStr
    email: EmailStr


class UserRequestAdd(UserBase):
    password: PasswordStr
    password2: PasswordStr

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.password2:
            raise ValueError("Passwords do not match")
        return self


class UserLogin(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: PasswordStr


class UserAdd(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    role_id: int
    is_active: bool


class UserWithHashPassword(User):
    hashed_password: str


class UserBaseUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: NameStr | None = None
    middle_name: NameStr | None = None
    last_name: NameStr | None = None
    email: EmailStr | None = None

    @model_validator(mode="after")
    def validate(self):
        if not self.model_dump(exclude_none=True):
            raise ValueError("At least one field must be provided")


class UserRequestUpdate(UserBaseUpdate):
    old_password: PasswordStr | None = None
    new_password: PasswordStr | None = None
    new_password2: PasswordStr | None = None

    @model_validator(mode="after")
    def validate(self):
        if self.old_password:
            if not self.new_password:
                raise ValueError("new_password is required")
            if not self.new_password2:
                raise ValueError("new_password2 is required")
            if self.new_password != self.new_password2:
                raise ValueError("Passwords do not match")
        return self


class UserUpdate(UserBaseUpdate):
    hashed_password: str | None = None
