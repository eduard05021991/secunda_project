# src/api/v1/organization/repository.py
from typing import AsyncGenerator
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from api.v1.organization.model import Organization, PhoneNumber
from api.v1.base.repository import BaseRepository
from api.v1.activity.model import Activity
from api.v1.activity.repository import ActivityRepository
from api.v1.building.model import Building
from db.session import get_async_session

from math import radians, cos, sin, asin, sqrt


class OrganizationRepository(BaseRepository):
    async def get_all(self):
        result = await self._execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building)
            )
        )
        return result.scalars().all()
    
    async def get_by_id(self, org_id: int):
        result = await self._execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building)
            )
            .where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()
    
    async def search_by_name(self, name_substring: str):
        result = await self._execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building)
            )
            .where(Organization.name.ilike(f"%{name_substring}%"))
        )
        return result.scalars().all()
    
    async def get_by_building(self, building_id: int):
        result = await self._execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building)
            )
            .where(Organization.building_id == building_id)
        )
        return result.scalars().all()

#    async def get_by_activity_with_children(self, activity_id: int):
#        # Рекурсивно собираем все дочерние ID
#        async def collect_ids(start_id: int, acc: set[int]):
#            acc.add(start_id)
#            result = await self._execute(
#                select(Activity.id).where(Activity.parent_id == start_id)
#            )
#            children_ids = [row[0] for row in result.all()]
#            for cid in children_ids:
#                await collect_ids(cid, acc)
#
#        all_ids = set()
#        await collect_ids(activity_id, all_ids)
#
#        # Запрос всех организаций по этим activity_ids
#        result = await self._execute(
#            select(Organization).distinct()
#            .options(
#                selectinload(Organization.phone_numbers),
#                selectinload(Organization.activities),
#                selectinload(Organization.building)
#            )
#            .join(Organization.activities)
#            .where(Activity.id.in_(all_ids))
#        )
#        return result.scalars().all()

    async def get_by_activity_with_children(self, activity_id: int):

        # Получаем все ID этой активности и всех её потомков
        activity_repo = ActivityRepository(self._session)
        all_ids = await activity_repo.get_all_descendant_ids(activity_id)

        # Запрос всех организаций по этим activity_ids
        result = await self._execute(
            select(Organization).distinct()
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building)
            )
            .join(Organization.activities)
            .where(Activity.id.in_(all_ids))
        )
        return result.scalars().all()

    async def get_by_location(self,
                              center_lat: float = None,
                              center_lon: float = None,
                              radius_km: float = None,
                              min_lat: float = None,
                              max_lat: float = None,
                              min_lon: float = None,
                              max_lon: float = None):

#        query = select(Organization).options(
#            selectinload(Organization.phone_numbers),
#            selectinload(Organization.activities),
#            selectinload(Organization.building)
#        ).join(Organization.building)
#
#        # Радиус
#        if center_lat is not None and center_lon is not None and radius_km is not None:
#            def haversine(lat1, lon1, lat2, lon2):
#                R = 6371
#                dlat = radians(lat2 - lat1)
#                dlon = radians(lon2 - lon1)
#                a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
#                return 2 * R * asin(sqrt(a))
#            # фильтр по Python из-за формулы (при большом объеме — выносить в SQL)
#            all_orgs = (await self._execute(query)).scalars().all()
#            return [
#                org for org in all_orgs
#                if haversine(center_lat, center_lon,
#                            org.building.latitude, org.building.longitude) <= radius_km
#            ]
#
#        # Прямоугольная область
#        if None not in (min_lat, max_lat, min_lon, max_lon):
#            query = query.where(
#                and_(
#                    Building.latitude >= min_lat,
#                    Building.latitude <= max_lat,
#                    Building.longitude >= min_lon,
#                    Building.longitude <= max_lon
#                )
#            )
#            result = await self._execute(query)
#            return result.scalars().all()

        query = select(Organization).options(
            selectinload(Organization.phone_numbers),
            selectinload(Organization.activities),
            selectinload(Organization.building)
        ).join(Organization.building)

        # Радиус через формулу хаверсина прямо в SQL
        if center_lat is not None and center_lon is not None and radius_km is not None:
            # Переводим радиус Земли в км
            earth_radius = 6371.0
            # Формула хаверсина
            distance_expr = earth_radius * func.acos(
                func.cos(func.radians(center_lat)) *
                func.cos(func.radians(Building.latitude)) *
                func.cos(func.radians(Building.longitude) - func.radians(center_lon)) +
                func.sin(func.radians(center_lat)) *
                func.sin(func.radians(Building.latitude))
            )
            query = query.where(distance_expr <= radius_km)

        # Прямоугольная область
        elif None not in (min_lat, max_lat, min_lon, max_lon):
            query = query.where(
                and_(
                    Building.latitude >= min_lat,
                    Building.latitude <= max_lat,
                    Building.longitude >= min_lon,
                    Building.longitude <= max_lon
                )
            )

        result = await self._execute(query)
        return result.scalars().all()

    async def create(self, name: str, building_id: int, phone_numbers: list[str], activity_ids: list[int]):
        org = Organization(name=name, building_id=building_id)

        # Добавляем телефоны
        for number in phone_numbers:
            org.phone_numbers.append(PhoneNumber(phone_number=number))

        # Привязываем деятельности по id
        if activity_ids:
            from api.v1.activity.model import Activity
            activities = (await self._execute(select(Activity).where(Activity.id.in_(activity_ids)))).scalars().all()
            org.activities.extend(activities)

        self._session.add(org)
        # await self._session.commit()
        await self._session.flush() # сохраняем в рамках текущей транзакции
        
        # await self._session.refresh(org)
        # return org
        # перегружаем org с подгрузкой нужных связей
        result = await self._execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building)
            )
            .where(Organization.id == org.id)
        )
        return result.scalar_one()


async def get_organization_repository() -> AsyncGenerator[OrganizationRepository, None]:
    async with get_async_session() as session:
        yield OrganizationRepository(session)
