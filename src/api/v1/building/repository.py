# src/api/v1/building/repository.py
from typing import AsyncGenerator
from sqlalchemy import select
from api.v1.building.model import Building
from api.v1.base.repository import BaseRepository
from db.session import get_async_session


class BuildingRepository(BaseRepository):
    async def get_all(self):
        result = await self._execute(select(Building))
        return result.scalars().all()

    async def create(self, address: str, latitude: float, longitude: float):
        new_building = Building(address=address, latitude=latitude, longitude=longitude)
        self._session.add(new_building)
        # await self._session.commit()
        await self._session.flush() # вместо commit — сохраняем в транзакцию
        await self._session.refresh(new_building)
        return new_building


async def get_building_repository() -> AsyncGenerator[BuildingRepository, None]:
    async with get_async_session() as session:
        yield BuildingRepository(session)
