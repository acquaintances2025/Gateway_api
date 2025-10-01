from fastapi import APIRouter, Response, Depends, Query, Request
from starlette.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import Annotated



from .path import AUTHORIZATION, REGISTRATION, CONFIRMATION, LOGOUT, PASSWORDRECOVERY, PASSWORDUPDATE

from src.domain import RegistrationUser, ConfirmationUser, AuthUser, PasswordUpdate
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
async def registration_user(user_data: RegistrationUser, response: Response):
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
                    value=answer.json()["data"]["refresh_token"],
                    httponly=True,
                    max_age=Config.TIME_COOKIES,
                    secure=True,
                    samesite="strict",
                )
                logger.info("Успешное выполнение запроса.")
                dic = answer.json()
                del dic["data"]["refresh_token"]
                return dic
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
                return JSONResponse(status_code=200, content=answer.json())
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=400, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе авторизации пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


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
                                          "access_token": "token"
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
async def authorization_user(user_data: AuthUser, response: Response):
    try:
        async with AgentAuthClient() as client:
            answer = await client.request(
                "POST",
                AUTHORIZATION,
                json=dict(user_data)
            )
            if answer.status_code == 200:
                response.delete_cookie(key="Hive")
                response.set_cookie(
                    key="Hive",
                    value=answer.json()["data"]["refresh_token"],
                    httponly=True,
                    max_age=Config.TIME_COOKIES,
                    secure=True,
                    samesite="strict",
                )
                logger.info("Успешное выполнение запроса.")
                dic = answer.json()
                del dic["data"]["refresh_token"]
                return dic
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=400, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})

@auth_router.get(LOGOUT)
async def user_logout(response: Response, request: Request):
    try:
        if request.cookies.get("Hive", None) is None:
            return JSONResponse(status_code=400, content={
                "isSuccess": False,
                "message": "Сессия пользователя не обнаружена.",
                "data": None
            })
        else:
            response.delete_cookie(key="Hive")
            return {
                "isSuccess": True,
                "message": "Успешное выполнение запроса",
                "data": None
            }
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})

@auth_router.get(PASSWORDRECOVERY)
async def user_password_recovery(email: str = Query(default=None, description="Email пользователя для восстановления пароля"),
                                 phone: str = Query(default=None, description="Номер телефона пользователя для восстановления пароля"),
                                 token: HTTPAuthorizationCredentials | None = Depends(security)):
    try:
        async with AgentAuthClient() as client:
            if token is not None:
                answer = await client.request(
                    "GET",
                    PASSWORDRECOVERY,
                    headers={"Authorization": f"Bearer {token.credentials}"}
                )
            else:
                params = {"email": email, "phone": phone}
                answer = await client.request(
                    "GET",
                    PASSWORDRECOVERY,
                    params=params
                )
            if answer.status_code == 200:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=200, content=answer.json())
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=400, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


@auth_router.post(PASSWORDUPDATE)
async def password_update(user_data: PasswordUpdate):
    try:
        async with AgentAuthClient() as client:
            answer = await client.request(
                "POST",
                PASSWORDUPDATE,
                json=dict(user_data),
            )
        if answer.status_code == 200:
            logger.info("Успешное выполнение запроса.")
            return JSONResponse(status_code=200, content=answer.json())
        else:
            logger.error(f"Ответ стороннего сервиса {answer.json()}")
            return JSONResponse(status_code=400, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе авторизации пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})