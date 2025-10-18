from pydantic import Field

from src.domain import BaseEntity

class ConfirmationPhone(BaseEntity):
    phone: str = Field(description="Номер телефона пользователя")