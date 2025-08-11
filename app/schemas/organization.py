from pydantic import BaseModel
from typing import List


class PhoneNumberBase(BaseModel):
    phone_number: str

class PhoneNumberCreate(PhoneNumberBase):
    pass

class PhoneNumber(PhoneNumberBase):
    id: int
    organization_id: int

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
    phone_numbers: List[PhoneNumber] = []

    class Config:
        from_attributes = True
