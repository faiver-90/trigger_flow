from fastapi import APIRouter, Depends, HTTPException

from src.modules.trigger.api.v1.get_service import get_trigger_service
from src.modules.trigger.api.v1.trigger_schemas import (
    TriggerCreate,
    TriggerOut,
    TriggerUpdate,
)
from src.modules.trigger.services.trigger_service import TriggerService
from src.modules.trigger.types.trigger_registry import TRIGGER_REGISTRY
from src.shared.deps.auth_dependencies import get_user_id

v1_trigger_router = APIRouter(
    prefix="/trigger",
    tags=["Triggers"],
    # dependencies=[Depends(authenticate_user)]
)


@v1_trigger_router.get(
    "/list_types",
    dependencies=[],
    summary="Список доступных типов триггеров",
    description="Возвращает список всех зарегистрированных типов триггеров и схемы параметров для каждого.",
)
async def list_trigger_types():
    return [
        {"name": name, "trigger_params": trigger.describe()}
        for name, trigger in TRIGGER_REGISTRY.items()
    ]


# @v1_trigger_router.post(
#     "/bulk-create",
#     summary="Создание триггеров с уведомлениями",
#     description="Создает множество триггеров и уведомлений для них в одном запросе.",
# )
# async def bulk_create_trigger(
#     data: BulkTriggerCreate, service: TriggerService = Depends(get_trigger_service)
# ):
#     return await service.bulk_create(data)


@v1_trigger_router.post(
    "/",
    response_model=TriggerOut,
    summary="Создание триггера",
    description="Создаёт новый триггера на основе входных данных.",
)
async def create_trigger(
    data: TriggerCreate,
    service: TriggerService = Depends(get_trigger_service),
    user_id: int = Depends(get_user_id),
):
    return await service.create(data.model_dump(), user_id)


@v1_trigger_router.get(
    "/{item_id}",
    response_model=TriggerOut,
    summary="Получение триггера по ID",
    description="Возвращает триггера по ID. Возвращает ошибку 404, если не найден.",
)
async def get_trigger(
    item_id: int,
    service: TriggerService = Depends(get_trigger_service),
    user_id: int = Depends(get_user_id),
):
    obj = await service.get(item_id, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_trigger_router.get(
    "/",
    response_model=list[TriggerOut],
    summary="Получение триггеров",
    description="Возвращает триггера по ID. Возвращает ошибку 404, если не найден.",
)
async def list_triggers(
    service: TriggerService = Depends(get_trigger_service),
    user_id: int = Depends(get_user_id),
):
    return await service.list(user_id)


@v1_trigger_router.put(
    "/{item_id}",
    response_model=TriggerOut,
    summary="Обновление триггера",
    description="Обновляет триггера по ID. Возвращает ошибку 404, если не найден.",
)
async def update_trigger(
    item_id: int,
    data: TriggerUpdate,
    service: TriggerService = Depends(get_trigger_service),
    user_id: int = Depends(get_user_id),
):
    obj = await service.update(item_id, data.model_dump(exclude_unset=True), user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_trigger_router.delete(
    "/{item_id}",
    summary="Удаление триггера",
    description="Удаляет триггера по ID. Возвращает ошибку 404, если не найден.",
)
async def delete_trigger(
    item_id: int,
    service: TriggerService = Depends(get_trigger_service),
    user_id: int = Depends(get_user_id),
):
    deleted = await service.delete(item_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
