from typing import Optional, List

from pydantic import BaseModel


class ActivityBase(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    level: int = 1


class ActivityCreate(BaseModel):
    name: str
    parent_id: int | None = None
    level: int = 1


class Activity(ActivityBase):
    id: int
    children: List["Activity"] = []

    class Config:
        from_attributes = True
