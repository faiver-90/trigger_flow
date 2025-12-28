from typing import Any

from pydantic import BaseModel, Field


class SourceBase(BaseModel):
    user_id: int
    source_type_id: int
    name: str
    config: dict[str, Any] = Field(default_factory=dict)
    is_active: bool


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    user_id: int | None = None
    source_type_id: int | None = None
    name: str | None = None
    config: dict[str, Any] | None = None
    is_active: bool | None = None


class SourceOut(SourceBase):
    id: int
    model_config = {"from_attributes": True}


class SourceTypeBase(BaseModel):
    name: str | None = None
    description: str | None = None
    config: dict[str, Any]


class SourceTypeCreate(SourceTypeBase):
    pass


class SourceTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    config: dict[str, Any] | None = None


class SourceTypeOut(SourceTypeBase):
    id: int
    model_config = {"from_attributes": True}
