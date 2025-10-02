from pickle import FALSE

from fastapi import APIRouter, Response, Depends, Query, Request
from starlette.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import Annotated


from src.infrastructure.docs import (logout,
                                     authorization,
                                     confirmation,
                                     password_recovery,
                                     refresh_update,
                                     registration,
                                     password_update)
from .path import AUTHORIZATION, REGISTRATION, CONFIRMATION, LOGOUT, PASSWORDRECOVERY, PASSWORDUPDATE, REFRESHUPDATE

from src.domain import RegistrationUser, ConfirmationUser, AuthUser, PasswordUpdate
from src.infrastructure import logger, AgentAuthClient

from src.config.settings import Config

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)



@auth_router.post(REGISTRATION, summary="Регистрация пользователя.",
                  response_description="Отправка письма/sms подтверждения регистрации.",
                  responses=registration)

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
                return JSONResponse(status_code=answer.status_code, content=answer.json())

    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})



@auth_router.post(CONFIRMATION,
                  summary="Подтверждение регистрации пользователя",
                  response_description="Аккаунт пользователя подтвержден, создана учетная запись в базе данных",
                  responses=confirmation)
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
                return JSONResponse(status_code=answer.status_code, content=answer.json())
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=answer.status_code, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе авторизации пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


@auth_router.post(AUTHORIZATION,
                  summary="Вход пользователя в аккаунт",
                  response_description="Создается сессия пользователя, в cookies прописывается refresh token",
                  responses=authorization)
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
                return JSONResponse(status_code=answer.status_code, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})

@auth_router.get(LOGOUT,
                  summary="Запрос выхода пользователя из аккаунта.",
                  response_description="Выход пользователя из сессии, зачистка cookies",
                  responses=logout)
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
                "message": "Успешное выполнение запроса.",
                "data": None
            }
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})

@auth_router.get(PASSWORDRECOVERY,
                  summary="Запрос на обновление пароля пользователя.",
                  response_description="Отправляет код подтверждения для обновления пароля пользователя. Работает как под авторизованным пользователем (через токен) так и под не авторизованным (под email)",
                  responses=password_recovery)
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
                return JSONResponse(status_code=answer.status_code, content=answer.json())
            else:
                logger.error(f"Ответ стороннего сервиса {answer.json()}")
                return JSONResponse(status_code=answer.status_code, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


@auth_router.post(PASSWORDUPDATE, summary="Завершение обновления пароля пользователя",
                  response_description="Обновление пароля пользователя от аккаунта",
                  responses=password_update)
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
            return JSONResponse(status_code=answer.status_code, content=answer.json())
        else:
            logger.error(f"Ответ стороннего сервиса {answer.json()}")
            return JSONResponse(status_code=answer.status_code, content=answer.json())
    except Exception as exc:
        logger.error(f"В процессе авторизации пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


@auth_router.get(REFRESHUPDATE, summary="Обновление токена доступа пользователя",
                  response_description="Обновляет access и refresh токен доступа, перезаписывает cookies",
                  responses=refresh_update)
async def refresh_update(response: Response, request: Request):
    try:
        if request.cookies.get("Hive", None) is None:
            return JSONResponse(status_code=401, content={
                "isSuccess": False,
                "message": "Сессия пользователя не обнаружена.",
                "data": None
            })
        else:
            async with AgentAuthClient() as client:
                answer = await client.request(
                    "GET",
                    REFRESHUPDATE,
                    cookies={"Hive": str(
                        request.cookies["Hive"]) if 'Hive' in request.cookies else None}
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
                    return JSONResponse(status_code=answer.status_code, content=answer.json())
                else:
                    logger.error(f"Ответ стороннего сервиса {answer.json()}")
                    return JSONResponse(status_code=answer.status_code, content=answer.json())

    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})