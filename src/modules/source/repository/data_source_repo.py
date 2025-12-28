from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.base_repo import BaseRepository
from src.shared.db import Sources


class DataSourceRepo(BaseRepository[Sources]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Sources)

    async def list(self, user_id: int | None = None):
        stmt = select(Sources)
        if user_id:
            stmt = stmt.where(Sources.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
