from typing import Any

from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    user_id: int | None = None
    notification_type_id: int | None = None
    name: str | None = None
    description: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)
    is_active: bool | None = None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    user_id: int | None = None
    notification_type_id: int | None = None
    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None
    is_active: bool | None = None


class NotificationOut(NotificationBase):
    id: int
    model_config = {"from_attributes": True}


class NotificationTypeBase(BaseModel):
    name: str | None = None
    description: str | None = None
    config: dict[str, Any]


class NotificationTypeCreate(NotificationTypeBase):
    pass


class NotificationTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None


class NotificationTypeOut(NotificationTypeBase):
    id: int
    model_config = {"from_attributes": True}
