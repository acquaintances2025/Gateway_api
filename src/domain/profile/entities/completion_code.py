from pydantic import Field

from src.domain import BaseEntity

class CompletionCode(BaseEntity):
    code: int = Field(description="Код подтверждений email/номера телефона пользователя")