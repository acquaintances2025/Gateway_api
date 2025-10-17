from fastapi import Request

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import JSONResponse

from .path import GET_PROFILE, DELETE_PROFILE, UPDATE_PROFILE


from src.domain import ProfileUser, UpdateProfile
from src.infrastructure import AgentProfileClient, logger, SessionData, verifier, cookie

profile_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)

security = HTTPBearer(auto_error=False)

@profile_router.get(GET_PROFILE, dependencies=[Depends(cookie)])
async def get_profiles(request: Request,
                       session_data: SessionData = Depends(verifier)):
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

@profile_router.put(UPDATE_PROFILE, dependencies=[Depends(cookie)])
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

@profile_router.delete(DELETE_PROFILE, dependencies=[Depends(cookie)])
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