from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.base_repo import BaseRepository
from src.shared.db import Triggers


class TriggerRepo(BaseRepository[Triggers]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Triggers)
