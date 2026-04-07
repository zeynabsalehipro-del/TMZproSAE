from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Voyage(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    
    # Relation One-to-One : Un voyage possède un seul budget
    budget = relationship("Budget", back_populates="trip", uselist=False)

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float)
    spent_amount = Column(Float, default=0.0)
    
    # Clé étrangère unique pour assurer la relation One-to-One
    trip_id = Column(Integer, ForeignKey("trips.id"), unique=True)
    trip = relationship("Voyage", back_populates="budget")
