# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def get_budget_by_trip(db: Session, trip_id: int):
    return db.query(models.Budget).filter(models.Budget.trip_id == trip_id).first()

def create_trip_budget(db: Session, budget: schemas.BudgetBase, trip_id: int):
    db_budget = models.Budget(**budget.dict(), trip_id=trip_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget
