from fastapi import Request

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import JSONResponse


from typing import List

from .path import GET_PROFILE, DELETE_PROFILE, UPDATE_PROFILE


from src.domain import ProfileUser, UpdateProfile
from src.infrastructure import AgentProfileClient, logger

profile_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)

security = HTTPBearer(auto_error=False)

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
async def get_profiles(request: Request,
                       token: HTTPAuthorizationCredentials | None = Depends(security)):
    try:
        async with AgentProfileClient() as client:
            answer = await client.request(
                "GET",
                GET_PROFILE,
                headers={"Authorization": f"Bearer {token.credentials}"}
            )
            if answer.status_code == 200:
                logger.info("Успешное выполнение запроса.")
                return JSONResponse(status_code=answer.status_code, content=answer.json())
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=answer.status_code, content=answer.json())

    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"isSuccess": False,
                                                      "message": "Возникла ошибка исполнения процесса.",
                                                      "data": {}})

@profile_router.put(UPDATE_PROFILE)
async def update_profile(request: Request,
                         user_data: UpdateProfile,
                         token: HTTPAuthorizationCredentials | None = Depends(security)):
    try:
        if user_data.birthday is not None:
            user_data.birthday = user_data.birthday.isoformat()

        async with AgentProfileClient() as client:
            answer = await client.request(
                "PUT",
                UPDATE_PROFILE,
                json=dict(user_data),
                headers={"Authorization": f"Bearer {token.credentials}"}
            )
            if answer.status_code == 200:
                logger.info("Успешное выполнение запроса.")
                return JSONResponse(status_code=answer.status_code, content=answer.json())
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=answer.status_code, content=answer.json())

    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"isSuccess": False,
                                                      "message": "Возникла ошибка исполнения процесса.",
                                                      "data": {}})

@profile_router.delete(DELETE_PROFILE)
async def delete_profile(token: HTTPAuthorizationCredentials | None = Depends(security)):
    try:
        async with AgentProfileClient() as client:
            answer = await client.request(
                "DELETE",
                DELETE_PROFILE,
                headers={"Authorization": f"Bearer {token.credentials}"}
            )
            if answer.status_code == 200:
                logger.info("Успешное выполнение запроса.")
                return JSONResponse(status_code=answer.status_code, content=answer.json())
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=answer.status_code, content=answer.json())

    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"isSuccess": False,
                                                      "message": "Возникла ошибка исполнения процесса.",
                                                      "data": {}})