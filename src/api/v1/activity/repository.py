# src/api/v1/activity/repository.py
from typing import AsyncGenerator

from sqlalchemy import select

from api.v1.activity.model import Activity
from api.v1.base.repository import BaseRepository
from db.session import get_async_session


class NotFoundError(Exception):
    pass


class ActivityRepository(BaseRepository):
    async def get_all_descendant_ids(self, activity_id: int) -> list[int]:
        """Возвращает список ID всех потомков указанного activity_id (включая его самого)."""
        from api.v1.activity.model import Activity

        found_ids = set()

        async def _collect(current_id: int):
            if current_id in found_ids:
                return
            found_ids.add(current_id)
            result = await self._execute(
                select(Activity.id).where(Activity.parent_id == current_id)
            )
            child_ids = [row[0] for row in result.all()]
            for cid in child_ids:
                await _collect(cid)

        await _collect(activity_id)
        return list(found_ids)
    
    async def get_activity_by_id(
            self,
            activity_id: int
    ):
        query = select(Activity).where(Activity.id == activity_id)
        result = await self._execute(query)
        return result.scalars().one_or_none()

    async def get_activities(
            self,
            activity_ids: list[int] | None = None
    ):
        query = select(Activity)
        if activity_ids:
            query = query.where(Activity.id.in_(activity_ids))
        result = await self._execute(query)
        return result.scalars().all()

    async def create_activity(
            self,
            name: str,
            parent_id: int | None = None,
            level: int = 1
    ):
        new_activity = Activity(name=name, parent_id=parent_id, level=level)
        self._session.add(new_activity)
        await self._session.commit()


async def get_activity_repository() -> AsyncGenerator[ActivityRepository, None]:
    async with get_async_session() as session:
        yield ActivityRepository(session)
