from fastapi import APIRouter, Depends, HTTPException

from src.modules.notifications.api.v1.get_service import (
    get_notification_service,
)
from src.modules.notifications.api.v1.schemas import (
    NotificationCreate,
    NotificationOut,
    NotificationUpdate,
)
from src.modules.notifications.services.notification_service import (
    CRUDNotificationService,
)
from src.modules.notifications.types.notifications_types_registry import (
    NOTIFY_REGISTRY,
)
from src.shared.deps.auth_dependencies import get_user_id

v1_notification_router = APIRouter(
    prefix="/notification",
    tags=["Notification"],
    # dependencies=[Depends(authenticate_user)]
)


@v1_notification_router.get(
    "/list_types",
    dependencies=[],
    summary="Список доступных типов уведомлений",
    description="Возвращает список всех зарегистрированных типов уведомлений и схемы параметров для каждого.",
)
async def list_notify_types():
    return [
        {"name": name, **notify.describe()} for name, notify in NOTIFY_REGISTRY.items()
    ]


@v1_notification_router.post(
    "/",
    response_model=NotificationOut,
    summary="Создание notification",
    description="Создаёт новый notification  на основе входных данных.",
)
async def create_notification(
    data: NotificationCreate,
    service: CRUDNotificationService = Depends(get_notification_service),
    user_id: int = Depends(get_user_id),
):
    return await service.create(data.model_dump(), user_id)


@v1_notification_router.get(
    "/{item_id}",
    response_model=NotificationOut,
    summary="Получение notification по ID",
    description="Возвращает notification по ID. Возвращает ошибку 404, если не найден.",
)
async def get_notification(
    item_id: int,
    service: CRUDNotificationService = Depends(get_notification_service),
    user_id: int = Depends(get_user_id),
):
    obj = await service.get(item_id, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_notification_router.get(
    "/",
    response_model=list[NotificationOut],
    summary="Получение notification",
    description="Возвращает notification по ID. Возвращает ошибку 404, если не найден.",
)
async def list_notification(
    service: CRUDNotificationService = Depends(get_notification_service),
    user_id: int = Depends(get_user_id),
):
    return await service.list(user_id=user_id)


@v1_notification_router.put(
    "/{item_id}",
    response_model=NotificationOut,
    summary="Обновление notification",
    description="Обновляет notification по ID. Возвращает ошибку 404, если не найден.",
)
async def update_notification(
    item_id: int,
    data: NotificationUpdate,
    service: CRUDNotificationService = Depends(get_notification_service),
    user_id: int = Depends(get_user_id),
):
    obj = await service.update(item_id, data.model_dump(exclude_unset=True), user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@v1_notification_router.delete(
    "/{item_id}",
    summary="Удаление notification",
    description="Удаляет notification по ID. Возвращает ошибку 404, если не найден.",
)
async def delete_notification(
    item_id: int,
    service: CRUDNotificationService = Depends(get_notification_service),
    user_id: int = Depends(get_user_id),
):
    deleted = await service.delete(item_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
