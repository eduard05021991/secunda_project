# src/api/v1/activity/model.py
from __future__ import annotations # откладывает разрешение имён классов

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from db.session import Base
"""
1	Еда		0
2	Мясная продукция	1	1
3	Молочная продукция	1	1
4	Автомобили		0
5	Грузовые	4	1
6	Легковые	4	1
"""

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"))
    level = Column(Integer, nullable=False, default=1)

    parent = relationship("Activity", remote_side=[id],
                          back_populates="children")
    children = relationship("Activity", back_populates="parent")

    organizations = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities"
    )

    __table_args__ = (CheckConstraint("level <= 3", name="max_level"),)


class OrganizationActivity(Base):
    __tablename__ = "organization_activities"

    organization_id = Column(Integer,
                             ForeignKey("organizations.id", ondelete="CASCADE"),
                             primary_key=True)
    activity_id = Column(Integer,
                         ForeignKey("activities.id", ondelete="CASCADE"),
                         primary_key=True)
