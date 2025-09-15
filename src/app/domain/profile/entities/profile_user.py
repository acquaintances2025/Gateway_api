from datetime import datetime
from typing import List

from app.domain import BaseEntity

class ProfileUser(BaseEntity):
    uuid: str
    tree_user: int | None
    name: str | None
    surname: str | None
    lastname: str | None
    age: int | None
    birthday: datetime
    place_birth: str|None
    number: str | None
    email: str | None
    images: List[str] | None

