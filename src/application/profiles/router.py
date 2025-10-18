from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from .path import GET_PROFILE, DELETE_PROFILE, UPDATE_PROFILE, CONFIRMATION_EMAIL, CONFIRMATION_PHONE, COMPLETION_CONFIRMATION
from src.infrastructure.docs import profile, update_profile, delete_profile, confirmation_email, confirmation_phone, completion_confirmation

from src.domain import ProfileUser, UpdateProfile, ConfirmationEmail, ConfirmationPhone, CompletionCode
from src.infrastructure import AgentProfileClient, logger, SessionData, verifier, cookie

profile_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)

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
                       responses=delete_profile
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
                    summary="Отправка кода подтверждения на email пользователя.",
                    response_description="Запрашивает email пользователя и отправляет код подтверждения.",
                    responses=confirmation_email
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


@profile_router.put(CONFIRMATION_PHONE,
                    dependencies=[Depends(cookie)],
                    summary="Отправка кода подтверждения на номер телефона пользователя.",
                    response_description="Запрашивает номер телефона пользователя и отправляет код подтверждения.",
                    responses=confirmation_phone
                       )
async def confirmation_phone(user_phone: ConfirmationPhone,
                             session_data: SessionData = Depends(verifier)):
    try:
        async with AgentProfileClient() as client:
            answer = await client.request(
                "PUT",
                CONFIRMATION_PHONE,
                json={"user_id": session_data.id, "phone": user_phone.phone}
            )
            if answer.status_code == 200:
                session_data.number = user_phone.phone
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

@profile_router.put(COMPLETION_CONFIRMATION,
                    dependencies=[Depends(cookie)],
                    summary="Подтверждение номера телефона пользователя.",
                    response_description="Запрашивает номер телефона пользователя и отправляет код подтверждения.",
                    responses=completion_confirmation
                    )
async def completion_confirmation(user_code: CompletionCode,
                                  session_data: SessionData = Depends(verifier)):
    try:
        async with AgentProfileClient() as client:
            answer = await client.request(
                "PUT",
                COMPLETION_CONFIRMATION,
                json={"user_id": session_data.id,
                      "phone": session_data.number,
                      "email": session_data.email,
                      "code": user_code.code}
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