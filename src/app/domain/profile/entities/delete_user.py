from pydantic import Field

from app.domain import BaseEntity

class DeleteUser(BaseEntity):
    uuid_user: str = Field(description="Идентификатор пользователя")