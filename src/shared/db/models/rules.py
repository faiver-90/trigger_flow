from sqlalchemy import ARRAY, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.shared.db.base import Base


class Rules(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    trigger_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_notification_ids: Mapped[list[int] | None] = mapped_column(
        ARRAY(Integer), nullable=True
    )
    is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    @validates("user_notification_ids")
    def sort_array(self, key, value):
        return sorted(value) if value else value
