from sqlalchemy.orm import Session

from models.building import Building as BuildingModel
from schemas.building import BuildingCreate


def create_building(db: Session, building: BuildingCreate) -> BuildingModel:
    db_building = BuildingModel(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


def get_building(db: Session, building_id: int) -> BuildingModel:
    return db.query(BuildingModel).filter(
        BuildingModel.id == building_id).first()


def get_buildings(db: Session, skip: int = 0, limit: int = 100) -> list[
    BuildingModel]:
    return db.query(BuildingModel).offset(skip).limit(limit).all()


def update_building(db: Session, building_id: int,
                    building: BuildingCreate) -> BuildingModel:
    db_building = db.query(BuildingModel).filter(
        BuildingModel.id == building_id).first()
    if not db_building:
        return None
    for key, value in building.dict().items():
        setattr(db_building, key, value)
    db.commit()
    db.refresh(db_building)
    return db_building


def delete_building(db: Session, building_id: int) -> bool:
    db_building = db.query(BuildingModel).filter(
        BuildingModel.id == building_id).first()
    if not db_building:
        return False
    db.delete(db_building)
    db.commit()
    return True
