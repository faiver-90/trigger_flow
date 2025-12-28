from typing import Generic, TypeVar

RepoType = TypeVar("RepoType")


class BaseCRUDService(Generic[RepoType]):
    def __init__(self, repo: RepoType):
        self.repo = repo

    async def create(self, data, user_id=None):
        if not data.get("user_id") or data["user_id"] == 0:
            data["user_id"] = user_id
        return await self.repo.create(data)

    async def get(self, obj_id: int, user_id=None):
        return await self.repo.get(obj_id, user_id)

    async def list(self, user_id=None):
        return await self.repo.list(user_id)

    async def update(self, obj_id: int, data, user_id=None):
        return await self.repo.update(obj_id, data, user_id)

    async def delete(self, obj_id: int, user_id=None):
        return await self.repo.delete(obj_id, user_id)
