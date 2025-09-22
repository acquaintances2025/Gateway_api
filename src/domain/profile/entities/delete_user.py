from pydantic import Field

from src.domain import BaseEntity

class DeleteUser(BaseEntity):
    uuid_user: str = Field(description="Идентификатор пользователя")