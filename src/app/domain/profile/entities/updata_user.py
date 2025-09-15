from pydantic import Field
from datetime import datetime
from typing import List

from app.domain import BaseEntity

class UpdateUser(BaseEntity):
    name: str = Field(default=None, description='Имя пользователя')
    surname: str = Field(default=None, description='Фамилия пользователя')
    lastname: str = Field(default=None, description='Отчество пользователя')
    age: int = Field(default=None, description='Возраст пользователя')
    birthday: datetime = Field(default=None, description='Дата рождения')
    place_birth: str = Field(default=None, description="Место рождения")
    number: str = Field(default=None, description='Номер телефона')
    email: str = Field(default=None, description='Email пользователя')
    images: List[str] = Field(default=None, description="Изображение пользователя")


