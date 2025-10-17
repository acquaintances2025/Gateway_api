from fastapi import Request, Query

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from httpx import ASGITransport
from starlette.responses import JSONResponse

from .path import GET_PROFILE, DELETE_PROFILE, UPDATE_PROFILE, CONFIRMATION_EMAIL, CONFIRMATION_PHONE
from src.infrastructure.docs import profile, update_profile, delete_profile

from src.domain import ProfileUser, UpdateProfile, ConfirmationEmail
from src.infrastructure import AgentProfileClient, logger, SessionData, verifier, cookie

profile_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)

security = HTTPBearer(auto_error=False)

@profile_router.get(GET_PROFILE,
                    dependencies=[Depends(cookie)],
                    summary="Получение аккаунта пользователя",
                    response_description="Отдает данные пользовательского профиля",
                    responses=profile)
async def get_profiles(session_data: SessionData = Depends(verifier)):
    try:
        async with AgentProfileClient() as client:
            answer = await client.request(
                "GET",
                GET_PROFILE,
                params={"user_id": session_data.id}
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

@profile_router.put(UPDATE_PROFILE,
                    dependencies=[Depends(cookie)],
                    summary="Обновление профиля пользователя",
                    response_description="Обновляет данные пользователя",
                    responses=update_profile)
async def update_profile(user_data: UpdateProfile,
                         session_data: SessionData = Depends(verifier)):
    try:
        if user_data.birthday is not None:
            user_data.birthday = user_data.birthday.isoformat()
        user_data = user_data.copy(update={"user_id": session_data.id})
        async with AgentProfileClient() as client:
            answer = await client.request(
                "PUT",
                UPDATE_PROFILE,
                json=dict(user_data)
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

@profile_router.delete(DELETE_PROFILE,
                       dependencies=[Depends(cookie)],
                       summary="Удаление профиля пользователя",
                       response_description="Переводит аккаунт пользователя в статус 'Удален' после чего включается счетчик активности, через 30 дней без активности профиль полностью удаляется",
                       # responses="delete_profile"
                       )
async def delete_profile(session_data: SessionData = Depends(verifier)):
    try:
        async with AgentProfileClient() as client:
            answer = await client.request(
                "DELETE",
                DELETE_PROFILE,
                params={"user_id": session_data.id}
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


@profile_router.put(CONFIRMATION_EMAIL,
                    dependencies=[Depends(cookie)],
                    summary="Подтверждение email пользователя.",
                    response_description="Запрашивает email пользователя и отправляет код подтверждения.",
                    # responses=delete_profile
                       )
async def confirmation_email(user_email: ConfirmationEmail,
                             session_data: SessionData = Depends(verifier)):
    try:
        async with AgentProfileClient() as client:
            answer = await client.request(
                "PUT",
                CONFIRMATION_EMAIL,
                json={"user_id": session_data.id, "email": user_email.email}
            )
            if answer.status_code == 200:
                session_data.email = user_email.email
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


@profile_router.get(CONFIRMATION_PHONE,
                    dependencies=[Depends(cookie)],
                    summary="Подтверждение номера телефона пользователя.",
                    response_description="Запрашивает номер телефона пользователя и отправляет код подтверждения.",
                    # responses=delete_profile
                       )
async def confirmation_phone(phone: str = Query(description="Email пользователя"),
                             session_data: SessionData = Depends(verifier)):
    try:
        session_data.number = phone
        async with AgentProfileClient() as client:
            answer = await client.request(
                "PUT",
                CONFIRMATION_PHONE,
                params={"phone": phone}
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