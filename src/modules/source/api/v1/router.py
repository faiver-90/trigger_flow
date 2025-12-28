import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from src.modules.source.api.v1.get_service import get_data_source_service
from src.modules.source.api.v1.schemas import (
    SourceCreate,
    SourceOut,
    SourceUpdate,
)
from src.modules.source.services.data_source_service import (
    CRUDDataSourceService,
)
from src.modules.source.types.data_source_registry import (
    DATA_SOURCE_REGISTRY,
)
from src.shared.decorators import log_action
from src.shared.deps.auth_dependencies import get_user_id

source_logger = logging.getLogger("source_log")

v1_api_source = APIRouter(
    prefix="/api_sources",
    tags=["API Sources"],
    # dependencies=[Depends(authenticate_user)]
)


@v1_api_source.get(
    "/list_types",
    # dependencies=[],
    summary="Список доступных АПИ",
    description="Возвращает список всех зарегистрированных АПИ.",
)
@log_action("message", logger=source_logger)
async def list_source_types():
    return [
        {"id": int(source_id), "name": config["name"], "config": config.get("data", {})}
        for source_id, config in DATA_SOURCE_REGISTRY.items()
    ]


@v1_api_source.post(
    "/",
    response_model=SourceOut,
    summary="Создание источника данных",
    description="Создаёт новый источник данных с указанными параметрами: имя, учётные данные и статус активности.",
)
async def create_api_source(
    data: SourceCreate,
    service: CRUDDataSourceService = Depends(get_data_source_service),
    user_id=Depends(get_user_id),
):
    return await service.create(data.model_dump(), user_id)


@v1_api_source.get(
    "/{source_id}",
    response_model=SourceOut,
    summary="Получить источник данных",
    description="Возвращает информацию об источнике данных по его ID. Если источник не найден — возвращает ошибку 404.",
)
async def get_api_source(
    source_id: int, service: CRUDDataSourceService = Depends(get_data_source_service)
):
    result = await service.get(source_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@v1_api_source.get(
    "/",
    response_model=list[SourceOut],
    summary="Список источников данных",
    description="Возвращает список всех источников данных. "
    "Можно указать параметр `user_id` для фильтрации по пользователю.",
)
async def list_api_sources(
    service: CRUDDataSourceService = Depends(get_data_source_service),
    user_id_query: int | None = Query(
        None, description="ID пользователя для фильтрации"
    ),
    user_id_token: int = Depends(get_user_id),
):
    user_id = user_id_query or user_id_token
    return await service.list(user_id)


@v1_api_source.put(
    "/{source_id}",
    response_model=SourceOut,
    summary="Обновить источник данных",
    description="Обновляет данные источника по его ID. Принимает изменённые поля и возвращает обновлённый объект."
    " Ошибка 404, если не найден.",
)
async def update_api_source(
    source_id: int,
    data: SourceUpdate,
    service: CRUDDataSourceService = Depends(get_data_source_service),
):
    updated = await service.update(source_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return updated


@v1_api_source.delete(
    "/{source_id}",
    summary="Удалить источник данных",
    description="Удаляет источник данных по ID. Если источник не найден — возвращает ошибку 404. "
    "Возвращает статус успешного удаления.",
)
async def delete_api_source(
    source_id: int, service: CRUDDataSourceService = Depends(get_data_source_service)
):
    deleted = await service.delete(source_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}
