from sqlalchemy.orm import Session

from models import Organization as OrganizationModel, PhoneNumber, OrganizationActivity
from schemas.organization import OrganizationCreate


def create_organization(db: Session,
                        organization: OrganizationCreate) -> OrganizationModel:
    db_organization = OrganizationModel(name=organization.name,
                                        building_id=organization.building_id)
    db.add(db_organization)
    db.flush()

    for phone in organization.phone_numbers:
        db_phone = PhoneNumber(organization_id=db_organization.id,
                               phone_number=phone.phone_number)
        db.add(db_phone)

    for activity_id in organization.activity_ids:
        db_activity = OrganizationActivity(organization_id=db_organization.id,
                                           activity_id=activity_id)
        db.add(db_activity)

    db.commit()
    db.refresh(db_organization)
    return db_organization


def get_organization(db: Session, organization_id: int) -> OrganizationModel:
    return db.query(OrganizationModel).filter(
        OrganizationModel.id == organization_id).first()


def get_organizations(db: Session, skip: int = 0, limit: int = 100) -> list[
    OrganizationModel]:
    return db.query(OrganizationModel).offset(skip).limit(limit).all()


def update_organization(db: Session, organization_id: int,
                        organization: OrganizationCreate) -> OrganizationModel:
    db_organization = db.query(OrganizationModel).filter(
        OrganizationModel.id == organization_id).first()
    if not db_organization:
        return None
    for key, value in organization.dict(
            exclude={"phone_numbers", "activity_ids"}).items():
        setattr(db_organization, key, value)

    # Update phone numbers
    db.query(PhoneNumber).filter(
        PhoneNumber.organization_id == organization_id).delete()
    for phone in organization.phone_numbers:
        db_phone = PhoneNumber(organization_id=organization_id,
                               phone_number=phone.phone_number)
        db.add(db_phone)

    # Update activities
    db.query(OrganizationActivity).filter(
        OrganizationActivity.organization_id == organization_id).delete()
    for activity_id in organization.activity_ids:
        db_activity = OrganizationActivity(organization_id=organization_id,
                                           activity_id=activity_id)
        db.add(db_activity)

    db.commit()
    db.refresh(db_organization)
    return db_organization


def delete_organization(db: Session, organization_id: int) -> bool:
    db_organization = db.query(OrganizationModel).filter(
        OrganizationModel.id == organization_id).first()
    if not db_organization:
        return False
    db.delete(db_organization)
    db.commit()
    return True


def get_organizations_by_building(db: Session, building_id: int) -> list[
    OrganizationModel]:
    return db.query(OrganizationModel).filter(
        OrganizationModel.building_id == building_id).all()


def get_organizations_by_activity(db: Session, activity_id: int) -> list[
    OrganizationModel]:
    return db.query(OrganizationModel).join(OrganizationActivity).filter(
        OrganizationActivity.activity_id == activity_id).all()


def get_organizations_by_activity_tree(db: Session, activity_id: int) -> list[
    OrganizationModel]:
    def get_activity_ids(activity_id: int, db: Session) -> list[int]:
        activity_ids = [activity_id]
        sub_activities = db.query(ActivityModel).filter(
            ActivityModel.parent_id == activity_id).all()
        for sub_activity in sub_activities:
            activity_ids.extend(get_activity_ids(sub_activity.id, db))
        return activity_ids

    activity_ids = get_activity_ids(activity_id, db)
    return db.query(OrganizationModel).join(OrganizationActivity).filter(
        OrganizationActivity.activity_id.in_(activity_ids)).all()


def search_organizations_by_name(db: Session, name: str) -> list[
    OrganizationModel]:
    return db.query(OrganizationModel).filter(
        OrganizationModel.name.ilike(f"%{name}%")).all()


def get_organizations_by_location(
        db: Session,
        latitude: float,
        longitude: float,
        radius: float = None,
        min_lat: float = None,
        max_lat: float = None,
        min_lon: float = None,
        max_lon: float = None
) -> list[OrganizationModel]:
    from sqlalchemy import func
    from math import radians, cos, sin

    if radius:
        earth_radius = 6371  # km
        lat1, lon1 = radians(latitude), radians(longitude)
        return db.query(OrganizationModel).join(BuildingModel).filter(
            func.acos(
                sin(lat1) * sin(func.radians(BuildingModel.latitude)) +
                cos(lat1) * cos(func.radians(BuildingModel.latitude)) *
                cos(func.radians(BuildingModel.longitude) - lon1)
            ) * earth_radius <= radius
        ).all()
    else:
        return db.query(OrganizationModel).join(BuildingModel).filter(
            BuildingModel.latitude.between(min_lat, max_lat),
            BuildingModel.longitude.between(min_lon, max_lon)
        ).all()
