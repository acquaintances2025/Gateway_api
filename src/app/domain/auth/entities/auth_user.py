from pydantic import Field

from app.domain import BaseEntity


class AuthUser(BaseEntity):
    number: str = Field(default=None, description="Номер телефона пользователя")
    email: str = Field(default=None, description="Eмейл пользователя")
    password: str = Field(description="Пароль пользователя")