from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.organization import (
    create_organization, get_organization, get_organizations,
    update_organization, delete_organization,
    get_organizations_by_building, get_organizations_by_activity,
    get_organizations_by_activity_tree,
    search_organizations_by_name, get_organizations_by_location
)
from database import get_db
from dependencies import verify_api_key
from schemas.organization import Organization, OrganizationCreate

router = APIRouter()


@router.post("/", response_model=Organization,
             summary="Создать новую организацию")
def create_organization_endpoint(organization: OrganizationCreate,
                                 db: Session = Depends(get_db),
                                 api_key: str = Depends(verify_api_key)):
    """Создает новую организацию с указанным названием, зданием, номерами телефонов и деятельностями."""
    return create_organization(db, organization)


@router.get("/", response_model=List[Organization],
            summary="Получить список организаций")
def get_organizations_endpoint(skip: int = 0, limit: int = 100,
                               db: Session = Depends(get_db),
                               api_key: str = Depends(verify_api_key)):
    """Возвращает список всех организаций с пагинацией."""
    return get_organizations(db, skip, limit)


@router.get("/{organization_id}", response_model=Organization,
            summary="Получить организацию по ID")
def get_organization_endpoint(organization_id: int,
                              db: Session = Depends(get_db),
                              api_key: str = Depends(verify_api_key)):
    """Возвращает информацию об организации по ее ID."""
    organization = get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.put("/{organization_id}", response_model=Organization,
            summary="Обновить организацию")
def update_organization_endpoint(organization_id: int,
                                 organization: OrganizationCreate,
                                 db: Session = Depends(get_db),
                                 api_key: str = Depends(verify_api_key)):
    """Обновляет информацию об организации по ее ID."""
    updated_organization = update_organization(db, organization_id,
                                               organization)
    if not updated_organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return updated_organization


@router.delete("/{organization_id}", summary="Удалить организацию")
def delete_organization_endpoint(organization_id: int,
                                 db: Session = Depends(get_db),
                                 api_key: str = Depends(verify_api_key)):
    """Удаляет организацию по ее ID."""
    success = delete_organization(db, organization_id)
    if not success:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"detail": "Organization deleted"}


@router.get("/by_building/{building_id}", response_model=List[Organization],
            summary="Получить организации по зданию")
def get_organizations_by_building_endpoint(building_id: int,
                                           db: Session = Depends(get_db),
                                           api_key: str = Depends(
                                               verify_api_key)):
    """Возвращает список организаций, находящихся в указанном здании."""
    return get_organizations_by_building(db, building_id)


@router.get("/by_activity/{activity_id}", response_model=List[Organization],
            summary="Получить организации по деятельности")
def get_organizations_by_activity_endpoint(activity_id: int,
                                           db: Session = Depends(get_db),
                                           api_key: str = Depends(
                                               verify_api_key)):
    """Возвращает список организаций, связанных с указанной деятельностью."""
    return get_organizations_by_activity(db, activity_id)


@router.get("/by_activity_tree/{activity_id}",
            response_model=List[Organization],
            summary="Получить организации по дереву деятельностей")
def get_organizations_by_activity_tree_endpoint(activity_id: int,
                                                db: Session = Depends(get_db),
                                                api_key: str = Depends(
                                                    verify_api_key)):
    """Возвращает список организаций, связанных с указанной деятельностью и всеми ее поддеятельностями."""
    return get_organizations_by_activity_tree(db, activity_id)


@router.get("/by_name/", response_model=List[Organization],
            summary="Поиск организаций по названию")
def search_organizations_by_name_endpoint(name: str,
                                          db: Session = Depends(get_db),
                                          api_key: str = Depends(
                                              verify_api_key)):
    """Возвращает список организаций, содержащих указанную строку в названии."""
    return search_organizations_by_name(db, name)


@router.get("/by_location/", response_model=List[Organization],
            summary="Получить организации по местоположению")
def get_organizations_by_location_endpoint(
        latitude: float,
        longitude: float,
        radius: float = None,
        min_lat: float = None,
        max_lat: float = None,
        min_lon: float = None,
        max_lon: float = None,
        db: Session = Depends(get_db),
        api_key: str = Depends(verify_api_key)
):
    """Возвращает список организаций в указанном радиусе или прямоугольной области."""
    if radius is None and (
            min_lat is None or max_lat is None or min_lon is None or max_lon is None):
        raise HTTPException(status_code=400,
                            detail="Either radius or bounding box parameters must be provided")
    return get_organizations_by_location(db, latitude, longitude, radius,
                                         min_lat, max_lat, min_lon, max_lon)
