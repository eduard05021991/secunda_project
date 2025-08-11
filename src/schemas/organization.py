from typing import List

from pydantic import BaseModel

from .activity import Activity
from .building import Building


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
    building: Building
    phone_numbers: List[PhoneNumber]
    activities: List[Activity]

    class Config:
        from_attributes = True
