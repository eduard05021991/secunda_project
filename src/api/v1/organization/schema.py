# src/api/v1/organization/schema.py
from typing import List

from pydantic import BaseModel

from api.v1.activity.schema import ActivityBase
from api.v1.building.schema import BuildingBase


class PhoneNumberBase(BaseModel):
    phone_number: str


class PhoneNumberCreate(PhoneNumberBase):
    pass


class PhoneNumber(PhoneNumberBase):
    id: int

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    name: str
    building_id: int
    phone_numbers: List[PhoneNumberCreate] = []
    activity_ids: List[int] = []


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: int
    building: BuildingBase
    phone_numbers: List[PhoneNumber]
    activities: List[ActivityBase]

    class Config:
        from_attributes = True
