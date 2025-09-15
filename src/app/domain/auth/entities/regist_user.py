import uuid

from pydantic import Field

from app.domain import BaseEntity

class RegistrationUser(BaseEntity):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    number: str = Field(default=None, description="Номер телефона пользователя")
    email: str = Field(default=None, description="Email пользователя")
    password: str = Field(description="Пароль пользователя")
    confirm_password: str = Field(description="Подтверждение пароля пользователя")

