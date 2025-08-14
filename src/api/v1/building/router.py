# src/api/v1/building/router.py
from fastapi import APIRouter, Depends, status
from typing import List
from api.v1.building.schema import Building, BuildingCreate
from api.v1.building.repository import BuildingRepository, get_building_repository

router = APIRouter()

from dependencies import verify_api_key


@router.get(
    "/",
    response_model=List[Building],
    summary="Список всех зданий",
    description="Возвращает список всех зданий",
)
async def get_all_buildings(repository: BuildingRepository = Depends(get_building_repository)):
    return await repository.get_all()

@router.post(
    "/",
    response_model=Building,
    status_code=status.HTTP_201_CREATED,
    summary="Создать здание",
    description="Создаёт новое здание с адресом и координатами",
)
async def create_building(
    building: BuildingCreate,
    repository: BuildingRepository = Depends(get_building_repository)
):
    return await repository.create(
        address=building.address,
        latitude=building.latitude,
        longitude=building.longitude
    )
