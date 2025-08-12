from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.building import create_building, get_building, get_buildings, \
    update_building, delete_building
from database import get_db
from dependencies import verify_api_key
from schemas.building import Building, BuildingCreate


router = APIRouter()

@router.post("/", response_model=Building, summary="Создать новое здание")
def create_building_endpoint(building: BuildingCreate,
                             db: Session = Depends(get_db),
                             api_key: str = Depends(verify_api_key)):
    """Создает новое здание с указанным адресом и координатами."""
    return create_building(db, building)

@router.get("/", response_model=List[Building],
            summary="Получить список зданий")
def get_buildings_endpoint(skip: int = 0, limit: int = 100,
                           db: Session = Depends(get_db),
                           api_key: str = Depends(verify_api_key)):
    """Возвращает список всех зданий с пагинацией."""
    return get_buildings(db, skip, limit)

@router.get("/{building_id}", response_model=Building,
            summary="Получить здание по ID")
def get_building_endpoint(building_id: int, db: Session = Depends(get_db),
                          api_key: str = Depends(verify_api_key)):
    """Возвращает информацию о здании по его ID."""
    building = get_building(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.put("/{building_id}", response_model=Building,
            summary="Обновить здание")
def update_building_endpoint(building_id: int, building: BuildingCreate,
                             db: Session = Depends(get_db),
                             api_key: str = Depends(verify_api_key)):
    """Обновляет информацию о здании по его ID."""
    updated_building = update_building(db, building_id, building)
    if not updated_building:
        raise HTTPException(status_code=404, detail="Building not found")
    return updated_building

@router.delete("/{building_id}", summary="Удалить здание")
def delete_building_endpoint(building_id: int, db: Session = Depends(get_db),
                             api_key: str = Depends(verify_api_key)):
    """Удаляет здание по его ID."""
    success = delete_building(db, building_id)
    if not success:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"detail": "Building deleted"}
