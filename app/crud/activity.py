from sqlalchemy.orm import Session
from ..models.activity import Activity as ActivityModel
from ..schemas.activity import ActivityCreate, Activity
from fastapi import HTTPException


def create_activity(db: Session, activity: ActivityCreate) -> ActivityModel:
    if activity.parent_id:
        parent = db.query(ActivityModel).filter(ActivityModel.id == activity.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent activity not found")
        if parent.level >= 3:
            raise HTTPException(status_code=400, detail="Maximum nesting level reached")
        activity.level = parent.level + 1
    
    db_activity = ActivityModel(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activity(db: Session, activity_id: int) -> ActivityModel:
    return db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()

def get_activities(db: Session, skip: int = 0, limit: int = 100) -> list[ActivityModel]:
    return db.query(ActivityModel).offset(skip).limit(limit).all()

def update_activity(db: Session, activity_id: int, activity: ActivityCreate) -> ActivityModel:
    db_activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    if not db_activity:
        return None
    if activity.parent_id:
        parent = db.query(ActivityModel).filter(ActivityModel.id == activity.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent activity not found")
        if parent.level >= 3:
            raise HTTPException(status_code=400, detail="Maximum nesting level reached")
        activity.level = parent.level + 1
    else:
        activity.level = 1
    for key, value in activity.dict().items():
        setattr(db_activity, key, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int) -> bool:
    db_activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    if not db_activity:
        return False
    db.delete(db_activity)
    db.commit()
    return True
