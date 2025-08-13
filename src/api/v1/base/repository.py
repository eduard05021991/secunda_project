from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query


class BaseRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _execute(self, query: Query) -> Result:
        return await self._session.execute(query)
