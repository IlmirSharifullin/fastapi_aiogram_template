from typing import Optional, cast

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..models import DBUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, user_id: int) -> Optional[DBUser]:
        return cast(
            Optional[DBUser],
            await self._session.scalar(select(DBUser).where(DBUser.id == user_id).options(joinedload('*'))),
        )

    async def get_by_username(self, username: str) -> Optional[DBUser]:
        return cast(
            Optional[DBUser],
            await self._session.scalar(select(DBUser).where(DBUser.username == username).options(joinedload('*'))),
        )

    async def create(self, tg_id: int, username: str):
        db_user = DBUser(id=tg_id,
                         username=username)

        await self.commit(db_user)
        return db_user
