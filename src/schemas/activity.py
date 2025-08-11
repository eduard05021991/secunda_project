from typing import Optional, List

from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    level: int = 1


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int
    children: List["Activity"] = []

    class Config:
        from_attributes = True
