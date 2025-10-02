from fastapi import APIRouter


from src.infrastructure.docs import healthz

test_router = APIRouter(tags=["healthz"])

@test_router.get("/healthz",  summary="Проверка работоспособности сервиса.",
                  response_description="Запрос проверки не лежит ли сервис.",
                  responses=healthz)
async def healthz():
    return {"status": "ok"}