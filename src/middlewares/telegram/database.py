from typing import Callable, Any

from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database import Repository


class DBSessionMiddleware(BaseMiddleware):
    session_pool: async_sessionmaker[AsyncSession]

    def __init__(
        self,
        session_pool: async_sessionmaker[AsyncSession]
    ) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable,
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['repository'] = Repository(session=session)
            return await handler(event, data)
