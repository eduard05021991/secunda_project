# src/api/v1/building/model.py
from __future__ import annotations # откладывает разрешение имён классов

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from db.session import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Связь с организациями (lazy='select' по умолчанию)
    organizations = relationship(
        "Organization", 
        back_populates="building"
    )
