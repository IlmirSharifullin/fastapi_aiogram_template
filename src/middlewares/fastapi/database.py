from typing import Any

from fastapi import Request
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.database import Repository


class FastApiDBSessionMiddleware:
    session_pool: async_sessionmaker[AsyncSession]

    def __init__(
            self,
            session_pool: async_sessionmaker[AsyncSession]
    ) -> None:
        self.session_pool = session_pool

    async def __call__(
            self,
            request: Request, call_next
    ) -> Any:
        async with self.session_pool() as session:
            repo = Repository(session=session)
            request.state.db = repo
            response = await call_next(request)
            return response
