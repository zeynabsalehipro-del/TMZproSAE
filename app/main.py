from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas

# Création des tables dans la base de données au démarrage
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="API de Planification de Voyage de Groupe",
    description="Projet SAE pour l'Université Sorbonne Paris Nord"
)

# Dépendance pour obtenir la session de la base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Général"])
def read_root():
    return {"message": "Bienvenue sur l'API Group Trip Planner !"}

# Route pour récupérer le budget d'un voyage spécifique
@app.get("/trips/{trip_id}/budget", tags=["Gestion du Budget"])
def get_trip_budget(trip_id: int, db: Session = Depends(get_db)):
    budget = db.query(models.Budget).filter(models.Budget.trip_id == trip_id).first()
    
    if not budget:
        raise HTTPException(
            status_code=404, 
            detail="Budget non trouvé pour ce voyage."
        )
    return budget

# Route pour mettre à jour les dépenses
@app.put("/trips/{trip_id}/budget", tags=["Gestion du Budget"])
def update_trip_budget(trip_id: int, budget_data: schemas.BudgetUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour le montant total ou les dépenses effectuées.
    """
    db_budget = db.query(models.Budget).filter(models.Budget.trip_id == trip_id).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget non trouvé.")
    
    # Mise à jour des champs
    db_budget.total_amount = budget_data.total_amount
    db_budget.spent_amount = budget_data.spent_amount
    
    db.commit()
    db.refresh(db_budget)
    return db_budget

    
    
