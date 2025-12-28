from typing import Any

from pydantic import BaseModel, Field


class TriggerBase(BaseModel):
    user_id: int | None = None
    source_id: int | None = None
    trigger_type_id: int | None = None
    name: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)
    is_active: bool | None = None


class TriggerCreate(TriggerBase):
    pass


class TriggerUpdate(BaseModel):
    user_id: int | None = None
    source_id: int | None = None
    trigger_type_id: int | None = None
    name: str | None = None
    config: dict[str, Any] | None = None
    is_active: bool | None = None


class TriggerOut(TriggerBase):
    id: int
    model_config = {"from_attributes": True}


class TriggerTypeBase(BaseModel):
    name: str | None = None
    description: str | None = None
    config: dict[str, Any]


class TriggerTypeCreate(TriggerTypeBase):
    pass


class TriggerTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None


class TriggerTypeOut(TriggerTypeBase):
    id: int
    model_config = {"from_attributes": True}
