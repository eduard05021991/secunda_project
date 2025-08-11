from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="RESTRICT"))
    
    building = relationship("Building", back_populates="organizations")
    phone_numbers = relationship("PhoneNumber", back_populates="organization")
    activities = relationship("Activity", secondary="organization_activities", back_populates="organizations")

class PhoneNumber(Base):
    __tablename__ = "phone_numbers"
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
    phone_number = Column(String(20), nullable=False)
    
    organization = relationship("Organization", back_populates="phone_numbers")
