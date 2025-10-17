from pydantic import Field

from src.domain import BaseEntity

class ConfirmationEmail(BaseEntity):
    email: str = Field(description="Email пользователя")
