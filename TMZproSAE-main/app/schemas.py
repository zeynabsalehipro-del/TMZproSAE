from pydantic import BaseModel
from typing import Optional

# Schéma de base pour le Budget
class BudgetBase(BaseModel):
    total_amount: float
    spent_amount: float = 0.0

# Schéma pour la mise à jour 
class BudgetUpdate(BaseModel):
    total_amount: Optional[float] = None
    spent_amount: Optional[float] = None

# Schéma pour la réponse API 
class BudgetResponse(BudgetBase):
    id: int
    trip_id: int

    class Config:
        from_attributes = True
