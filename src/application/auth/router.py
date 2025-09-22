from fastapi import APIRouter, Response, Depends
from starlette.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import Annotated



from .path import AUTHORIZATION, REGISTRATION, CONFIRMATION

from src.domain import RegistrationUser, ConfirmationUser, AuthUser
from src.infrastructure import logger, AgentAuthClient

from src.config.settings import Config

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)



@auth_router.post(REGISTRATION, summary="Регистрация пользователя",
                  response_description="Отправка письма/sms подтверждения",
                  responses={
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                        "isSuccess": True,
                        "message": "Код подтверждения успешно отправлен",
                        "data": {}
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
async def authorization_user(user_data: RegistrationUser, response: Response):
    try:
        user_data.birthday = user_data.birthday.isoformat()
        async with AgentAuthClient() as client:
            answer = await client.request(
                "POST",
                REGISTRATION,
                json=dict(user_data)
            )

            if answer.status_code == 200:
                response.delete_cookie(key="Hive")
                response.set_cookie(
                    key="Hive",
                    value=answer.json()["refresh_token"],
                    httponly=True,
                    max_age=Config.TIME_COOKIES,
                    secure=True,
                    samesite="strict",
                )
                logger.info("Успешное выполнение запроса.")
                return JSONResponse(status_code=200, content={"access_token": answer.json()["access_token"]})
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=400, content=answer.json())

    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})



@auth_router.post(CONFIRMATION,
                  summary="Подтверждение регистрации пользователя",
                  response_description="Аккаунт пользователя подтвержден, создана учетная запись в базе данных",
                  responses={
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                        "isSuccess": True,
                        "message": "Успешное подтверждение учетной запись",
                        "data": {}
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
async  def confirmation_user(code: ConfirmationUser,
                             token: HTTPAuthorizationCredentials | None = Depends(security)):
    try:
        async with AgentAuthClient() as client:
            answer = await client.request(
                "POST",
                CONFIRMATION,
                json=dict(code),
                headers={"Authorization": f"Bearer {token.credentials}"}
            )
            if answer.status_code == 200:
                logger.info("Успешное выполнение запроса.")
                return answer.json(), 200
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=400, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return None, 500


@auth_router.post(AUTHORIZATION,
                  summary="Вход пользователя в аккаунт",
                  response_description="Создается сессия пользователя, в cookies прописывается refresh token",
                  responses={
                      "200": {
                          "description": "Успешное выполнение запроса",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "isSuccess": True,
                                      "message": "Успешный вход в аккаунт",
                                      "data": {
                                          "acsses_token": "token"
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
async def authorization_user(user_data: AuthUser):
    try:
        async with AgentAuthClient() as client:
            response = await client.request(
                "POST",
                AUTHORIZATION,
                json=user_data
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