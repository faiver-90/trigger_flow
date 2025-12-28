from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.db.session import get_async_session


def base_get_service(service_class, repo_class, *extra_args):
    async def _get(session: AsyncSession = Depends(get_async_session)):
        repo = repo_class(session)
        return service_class(repo, *extra_args)

    return _get
