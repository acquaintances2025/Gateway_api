from fastapi import APIRouter

from .path import AUTHORIZATION, REGISTRATION, CONFIRMATION

from app.domain import RegistrationUser, ConfirmationUser, AuthUser
from app.infrastructure import logger, AgentAuthClient

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


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
async def authorization_user(user_data: RegistrationUser):
    try:
        async with AgentAuthClient() as client:
            response = await client.request(
                "POST",
                REGISTRATION,
                json=user_data
            )

            if response.status_code == 200:
                logger.info("Успешное выполнение запроса.")
                return response.json(), 200
            else:
                logger.error(f"Ответ стороннего сервиса {response.json()}")
                return response.json(), 400
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return None, 500



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
async  def confirmation_user(code: ConfirmationUser):
    try:
        async with AgentAuthClient() as client:
            response = await client.request(
                "POST",
                CONFIRMATION,
                json=code
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