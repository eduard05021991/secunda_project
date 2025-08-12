from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.activity import create_activity, get_activity, get_activities, \
    update_activity, delete_activity
from database import get_db
from dependencies import verify_api_key
from schemas.activity import Activity, ActivityCreate


router = APIRouter()

@router.post("/", response_model=Activity, summary="Создать новую деятельность")
def create_activity_endpoint(activity: ActivityCreate,
                             db: Session = Depends(get_db),
                             api_key: str = Depends(verify_api_key)):
    """Создает новую деятельность с учетом ограничения вложенности (максимум 3 уровня)."""
    return create_activity(db, activity)


@router.get("/", response_model=List[Activity],
            summary="Получить список деятельностей")
def get_activities_endpoint(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db),
                            api_key: str = Depends(verify_api_key)):
    """Возвращает список всех деятельностей с пагинацией."""
    return get_activities(db, skip, limit)


@router.get("/{activity_id}", response_model=Activity,
            summary="Получить деятельность по ID")
def get_activity_endpoint(activity_id: int, db: Session = Depends(get_db),
                          api_key: str = Depends(verify_api_key)):
    """Возвращает информацию о деятельности по ее ID."""
    activity = get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.put("/{activity_id}", response_model=Activity,
            summary="Обновить деятельность")
def update_activity_endpoint(activity_id: int, activity: ActivityCreate,
                             db: Session = Depends(get_db),
                             api_key: str = Depends(verify_api_key)):
    """Обновляет информацию о деятельности по ее ID."""
    updated_activity = update_activity(db, activity_id, activity)
    if not updated_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated_activity


@router.delete("/{activity_id}", summary="Удалить деятельность")
def delete_activity_endpoint(activity_id: int, db: Session = Depends(get_db),
                             api_key: str = Depends(verify_api_key)):
    """Удаляет деятельность по ее ID."""
    success = delete_activity(db, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"detail": "Activity deleted"}
