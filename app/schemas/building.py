from pydantic import BaseModel
from typing import Optional


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int
    
    class Config:
        from_attributes = True
