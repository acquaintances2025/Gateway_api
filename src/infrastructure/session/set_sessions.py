from uuid import uuid4

from fastapi.responses import JSONResponse


from ..proxy.proxy_client import AgentProfileClient
from ..loggings.logger import logger
from ..security.jwt_prowider import decode_token

from ..session.confirm_session import SessionData, backend, cookie



async def set_session(user_token: str, response):
    payload, _ = await decode_token(user_token)
    async with AgentProfileClient() as client:
        answer = await client.request(
            "GET",
            "/profile",
            params={"user_id": payload["user_id"]}
        )
        if answer.status_code == 200:
            user_data = answer.json()["data"]
            session = uuid4()
            data = SessionData(id=user_data["id"],
                               uuid=user_data["uuid"],
                               name=user_data["name"],
                               lastname=user_data["lastname"],
                               surname=user_data["surname"],
                               email=user_data["email"],
                               number=user_data["number"],
                               active=user_data["active"],
                               active_phone=user_data["active_phone"],
                               active_email=user_data["active_email"])

            await backend.create(session, data)
            cookie.attach_to_response(response, session)
            return True
        else:
            pass
            logger.error(f"Ответ стороннего сервиса {answer.json()}")
            return JSONResponse(status_code=answer.status_code, content=answer.json())