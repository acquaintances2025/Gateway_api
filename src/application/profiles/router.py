from fastapi import Request

from fastapi import APIRouter

from typing import List

from .path import GET_PROFILE, DELETE_PROFILE, UPDATE_PROFILE

from src.domain import ProfileUser
from src.infrastructure import AgentProfileClient, logger

profile_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)

@profile_router.get(GET_PROFILE,
                    summary="Получение профиль пользователя",
                    # response_model=List[ProfileUser],
                    response_description="Возврат данных аккаунта пользователя",
                    responses={
                      "200": {
                          "description": "Успешное выполнение запроса",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "isSuccess": True,
                                      "message": "Профиль пользователя",
                                      "data": {
                                          "uuid": "str",
                                          "tree_user": "",
                                          "name": "",
                                          "surname": "",
                                          "lastname": "",
                                          "age": "",
                                          "birthday": "",
                                          "place_birth": "",
                                          "number": "",
                                          "email": "",
                                          "images": "",
                                      }
                                  }
                              }
                          }
                      },
                      "400": {
                          "description": "Ошибка в запросе"
                      },
                      "500": {
                          "description": "Внутренняя ошибка сервера"
                      }
                  })
async def get_profiles(request: Request):
    # todo добавить систему проверку наличия авторизации на старте запроса
    try:
        async with AgentProfileClient() as client:
            response = await client.request(
                "GET",
                GET_PROFILE,
                json={} #todo решить что отправлять на сервис профиля либо jwt token и раскодировать его там либо раскодировать его тут и отправлять uuid пользователя
            )
            if response.status_code == 200:
                logger.info("Успешное выполнение запроса.")
                return response.json(), 200
            else:
                logger.error(f"Ответ стороннего сервиса {response.json()}")
                return response.json(), 400
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return None, 500