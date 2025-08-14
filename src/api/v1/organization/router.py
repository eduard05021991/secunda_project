# src/api/v1/organization/router.py
from fastapi import APIRouter, Depends, status, Query
from typing import List
from api.v1.organization.schema import Organization, OrganizationCreate
from api.v1.organization.repository import OrganizationRepository, get_organization_repository
from dependencies import verify_api_key


router = APIRouter(
    # dependencies=[Depends(verify_api_key)]
)

@router.get(
    "/",
    response_model=List[Organization],
    summary="Список организаций",
    description="Возвращает список всех организаций с данными по зданиям, телефонам и видам деятельности.",
)
async def list_organizations(repo: OrganizationRepository = Depends(get_organization_repository)):
    return await repo.get_all()

@router.get(
    "/{org_id:int}",
    response_model=Organization,
    summary="Получить организацию по ID",
    description="Возвращает одну организацию по ID.",
)
async def get_organization_by_id(org_id: int, repo: OrganizationRepository = Depends(get_organization_repository)):
    org = await repo.get_by_id(org_id)
    if org is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Организация не найдена!")
    return org

@router.get(
    "/search/by-name",
    response_model=List[Organization],
    summary="Поиск организации по названию",
    description="Возвращает список организаций, название которых содержит указанную подстроку. "
                "Поиск регистронезависимый.",
)
async def search_organizations_by_name(
    name: str = Query(..., description="Часть или полное название организации для поиска", example="Рога"),
    repo: OrganizationRepository = Depends(get_organization_repository)
):
    return await repo.search_by_name(name)

@router.get(
    "/by-building/{building_id}",
    response_model=List[Organization],
    summary="Список организаций в конкретном здании",
    description="Все организации в указанном здании",
)
async def list_organizations_by_building(building_id: int, repo: OrganizationRepository = Depends(get_organization_repository)):
    return await repo.get_by_building(building_id)

@router.get(
    "/by-activity/{activity_id}",
    response_model=List[Organization],
    summary="Список организаций по видам деятельности (с потомками)",
    description="Организации по указанному виду деятельности и всем его потомкам",
)
async def list_organizations_by_activity_with_children(activity_id: int, repo: OrganizationRepository = Depends(get_organization_repository)):
    return await repo.get_by_activity_with_children(activity_id)

@router.get(
    "/by-location",
    response_model=List[Organization],
    summary="Поиск организаций по координатам зданий (радиус или прямоугольник)",
    description="Организации по указанному виду деятельности и всем его потомкам",
)
async def list_organizations_by_location(center_lat: float | None = None, center_lon: float | None = None, radius_km: float | None = None, min_lat: float | None = None, max_lat: float | None = None, min_lon: float | None = None, max_lon: float | None = None, repo: OrganizationRepository = Depends(get_organization_repository)):
    return await repo.get_by_location(center_lat, center_lon, radius_km, min_lat, max_lat, min_lon, max_lon)

@router.post(
    "/",
    response_model=Organization,
    status_code=status.HTTP_201_CREATED,
    summary="Создать организацию",
    description="Создаёт новую организацию с привязкой к зданию, телефонам и видам деятельности",
)
async def create_organization(
    org_data: OrganizationCreate,
    repo: OrganizationRepository = Depends(get_organization_repository)
):
    return await repo.create(
        name=org_data.name,
        building_id=org_data.building_id,
        phone_numbers=[p.phone_number for p in org_data.phone_numbers],
        activity_ids=org_data.activity_ids
    )
