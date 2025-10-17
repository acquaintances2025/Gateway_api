from fastapi import Response
from fastapi.responses import JSONResponse

from src.config.settings import Config

from src.infrastructure import decode_token


class Middleware(object):
    def __init__(self, request, call_next):
        self.request = request
        self.call_next = call_next

    async def check_tokens(self):
        if self.request.url.path in Config.IGNORE_PATH:
            response = await self.call_next(self.request)
            return response
        else:
            if self.request.headers.get("authorization", None) is not None:
                payload, error = await decode_token(self.request.headers["authorization"].split("Bearer ")[1])
                if payload is not None:
                    if payload["role"] == "admin":
                        response = await self.call_next(self.request)
                        return response
                    elif payload["role"] == "support" and self.request.url.path not in Config.FORBIDDEN_SUPPORT_PATH:
                        response = await self.call_next(self.request)
                        return response
                    elif payload["role"] == "user" and self.request.url.path not in Config.FORBIDDEN_USER_PATH:
                        response = await self.call_next(self.request)
                        return response
                    else:
                        return JSONResponse(
                            status_code=401, content={
                                "isSuccess": False,
                                "message": "У вас нет доступа к данному запросу.",
                                "data": {}
                            })

                else:
                    return JSONResponse(
                        status_code=401, content={
                            "isSuccess": False,
                            "message": "Токен пользователя не действителен.",
                            "data": {}
                        })
            else:
                return JSONResponse(
                    status_code=401, content={
                        "isSuccess": False,
                        "message": "Отсутствует токен авторизации пользователя.",
                        "data": {}
                    })

