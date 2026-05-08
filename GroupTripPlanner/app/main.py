# =============================================================
# main.py — Point d'entrée de l'API Group Trip Planner
# Projet SAE — Université Sorbonne Paris Nord
#
# Regroupe les routes des trois membres :
#   - Membre A (Mathurin) : Utilisateurs, Voyages, Relations
#   - Membre B (Teodora)   : Destinations (One-to-Many avec Voyages)
#   - Membre C (Zeynab)   : Budget (One-to-One avec Voyages)
# =============================================================

from datetime import date as date_type
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from . import models, database, schemas, crud
from .verification import (
    verifier_email, verifier_str, verifier_int,
    verifier_date, verifier_existence_email,
    verifier_existence_id, verification_utilisateur, verification_voyage
)

# Création de toutes les tables au démarrage
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Group Trip Planner",
    description=(
        "Projet SAE — Université Sorbonne Paris Nord\n\n"

    ),
    version="1.0.0"
)

# ----------------------------------------------------------
# Configuration CORS — autorise les appels du front-end
# ----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------
# Dépendance de session base de données
# ----------------------------------------------------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================================================
# ROUTE RACINE
# =============================================================

@app.get("/api", tags=["Général"])
def home():
    return {
        "message": "Bienvenue dans l'API Group Trip Planner!",
        "champs_utiles": {
            "Utilisateurs": "utilisateur_id, email (x@y.z), prenom, nom, age, mdp",
            "Voyages":      "voyage_id, jour, mois, annee, lieu, voyage_fini, prix",
            "Relations":    "utilisateur_id, voyage_id",
            "Destinations": "destination_id, nom, localisation, categorie, notes, ordre, voyage_id",
            "Budget":       "id, total_amount, spent_amount, trip_id (= voyage_id)"
        }
    }


# =============================================================
# MEMBRE A (Mathurin) — UTILISATEURS
# Routes portées de API_REST_PostgreSQL_Utilisateur_Voyage_Relation_FastAPI.py
# =============================================================

@app.post("/utilisateurs", tags=["Utilisateurs"])
def post_utilisateur(infos: dict, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur."""
    if not all(k in infos for k in ("email", "prenom", "nom", "age", "mdp")):
        raise HTTPException(status_code=400, detail="Le json doit contenir l'email, le prénom, le nom, l'âge et le mot de passe!")

    message = verifier_email(infos["email"])
    if message != "OK":
        raise HTTPException(status_code=400, detail=message)

    if verifier_existence_email(db, infos["email"]):
        raise HTTPException(status_code=400, detail="L'email existe déjà!")

    for champ in ("prenom", "nom", "mdp"):
        message = verifier_str(infos[champ], champ)
        if message != "OK":
            raise HTTPException(status_code=400, detail=message)

    if not isinstance(infos["age"], int):
        raise HTTPException(status_code=400, detail="Un age doit être un Integer!")
    if infos["age"] < 0:
        raise HTTPException(status_code=400, detail="L'âge doit être supérieur ou égal à 0!")

    return crud.create_utilisateur(db, infos).to_dict()


@app.get("/utilisateurs", tags=["Utilisateurs"])
def get_utilisateurs(db: Session = Depends(get_db)):
    """Lister tous les utilisateurs."""
    return [u.to_dict() for u in crud.get_all_utilisateurs(db)]


@app.get("/utilisateurs/all/{email}", tags=["Utilisateurs"])
def get_all_by_email(email: str, db: Session = Depends(get_db)):
    """Récupérer toutes les infos d'un utilisateur par son email."""
    u = crud.get_utilisateur_by_email(db, email)
    if not u:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas!")
    return u.to_dict()


@app.get("/utilisateurs/nom/{email}", tags=["Utilisateurs"])
def get_nom_by_email(email: str, db: Session = Depends(get_db)):
    u = crud.get_utilisateur_by_email(db, email)
    if not u:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas!")
    return {"nom": u.nom}


@app.get("/utilisateurs/prenom/{email}", tags=["Utilisateurs"])
def get_prenom_by_email(email: str, db: Session = Depends(get_db)):
    u = crud.get_utilisateur_by_email(db, email)
    if not u:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas!")
    return {"prenom": u.prenom}


@app.get("/utilisateurs/age/{email}", tags=["Utilisateurs"])
def get_age_by_email(email: str, db: Session = Depends(get_db)):
    u = crud.get_utilisateur_by_email(db, email)
    if not u:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas!")
    return {"age": u.age}


@app.put("/utilisateurs/{email}", tags=["Utilisateurs"])
def put_utilisateur(email: str, infos: dict, db: Session = Depends(get_db)):
    """Mettre à jour un ou plusieurs champs d'un utilisateur."""
    if not crud.get_utilisateur_by_email(db, email):
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas!")

    email_courant = email
    for cle, valeur in infos.items():
        if cle in ("email", "prenom", "nom", "age", "mdp"):
            message = verification_utilisateur(cle, valeur)
            if message != "OK":
                raise HTTPException(status_code=400, detail=message)
            if cle == "email" and verifier_existence_email(db, valeur):
                raise HTTPException(status_code=400, detail="L'email existe déjà!")
            crud.modifier_utilisateur(db, email_courant, cle, valeur)
            if cle == "email":
                email_courant = valeur

    u = crud.get_utilisateur_by_email(db, email_courant)
    return u.to_dict()


@app.delete("/utilisateurs/{email}", tags=["Utilisateurs"])
def delete_utilisateur(email: str, db: Session = Depends(get_db)):
    """Supprimer un utilisateur par son email."""
    message = verifier_email(email)
    if message != "OK":
        raise HTTPException(status_code=400, detail=message)
    deleted = crud.supprimer_utilisateur(db, email)
    if not deleted:
        raise HTTPException(status_code=404, detail="L'email n'existe pas!")
    return {"message": f"Utilisateur '{email}' supprimé avec succès."}


# =============================================================
# MEMBRE A (Mathurin) — VOYAGES
# =============================================================

@app.post("/voyages", tags=["Voyages"])
def post_voyage(infos: dict, db: Session = Depends(get_db)):
    """Créer un nouveau voyage."""
    if not all(k in infos for k in ("jour", "mois", "annee", "lieu", "prix")):
        raise HTTPException(status_code=400, detail="Le json doit contenir le jour, le mois, l'année, le lieu et le prix!")

    message = verifier_date(infos["jour"], infos["mois"], infos["annee"])
    if message != "OK":
        raise HTTPException(status_code=400, detail=message)

    message = verifier_str(infos["lieu"], "lieu")
    if message != "OK":
        raise HTTPException(status_code=400, detail=message)

    if not isinstance(infos["prix"], (int, float)):
        raise HTTPException(status_code=400, detail="Un prix doit être un Integer ou un Float!")
    if infos["prix"] < 0:
        raise HTTPException(status_code=400, detail="Un prix ne peut pas être négatif!")

    return crud.create_voyage(db, infos).to_dict()


@app.get("/voyages", tags=["Voyages"])
def get_voyages(db: Session = Depends(get_db)):
    """Lister tous les voyages."""
    return [v.to_dict() for v in crud.get_all_voyages(db)]


@app.get("/voyages/all/{voyage_id}", tags=["Voyages"])
def get_all_by_voyage_id(voyage_id: int, db: Session = Depends(get_db)):
    """Récupérer toutes les infos d'un voyage par son ID."""
    v = crud.get_voyage_by_id(db, voyage_id)
    if not v:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas!")
    return v.to_dict()


@app.get("/voyages/lieu/{voyage_id}", tags=["Voyages"])
def get_lieu_by_voyage_id(voyage_id: int, db: Session = Depends(get_db)):
    v = crud.get_voyage_by_id(db, voyage_id)
    if not v:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas!")
    return {"lieu": v.lieu}


@app.get("/voyages/prix/{voyage_id}", tags=["Voyages"])
def get_prix_by_voyage_id(voyage_id: int, db: Session = Depends(get_db)):
    v = crud.get_voyage_by_id(db, voyage_id)
    if not v:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas!")
    return {"prix": float(v.prix)}


@app.get("/voyages/voyage_fini/{voyage_id}", tags=["Voyages"])
def get_voyage_fini_by_voyage_id(voyage_id: int, db: Session = Depends(get_db)):
    v = crud.get_voyage_by_id(db, voyage_id)
    if not v:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas!")
    return {"voyage_fini": v.voyage_fini}


@app.put("/voyages/{voyage_id}", tags=["Voyages"])
def put_voyage(voyage_id: int, infos: dict, db: Session = Depends(get_db)):
    """Mettre à jour un ou plusieurs champs d'un voyage."""
    if not crud.get_voyage_by_id(db, voyage_id):
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas!")

    for cle, valeur in infos.items():
        if cle in ("prix", "voyage_fini", "lieu"):
            message = verification_voyage(cle, valeur)
            if message != "OK":
                raise HTTPException(status_code=400, detail=message)
            crud.modifier_voyage(db, voyage_id, cle, valeur)

    if all(k in infos for k in ("jour", "mois", "annee")):
        message = verifier_date(infos["jour"], infos["mois"], infos["annee"])
        if message != "OK":
            raise HTTPException(status_code=400, detail=message)
        nouvelle_date = date_type(infos["annee"], infos["mois"], infos["jour"])
        crud.modifier_voyage(db, voyage_id, "date", nouvelle_date)

    return crud.get_voyage_by_id(db, voyage_id).to_dict()


@app.delete("/voyages/{voyage_id}", tags=["Voyages"])
def delete_voyage(voyage_id: int, db: Session = Depends(get_db)):
    """Supprimer un voyage (et toutes ses destinations en cascade)."""
    deleted = crud.supprimer_voyage(db, voyage_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas!")
    return {"message": f"Voyage id={voyage_id} supprimé avec succès."}


# =============================================================
# MEMBRE A (Mathurin) — RELATIONS
# =============================================================

@app.post("/relations", tags=["Relations"])
def post_relation(infos: dict, db: Session = Depends(get_db)):
    """Associer un utilisateur à un voyage."""
    if not all(k in infos for k in ("utilisateur_id", "voyage_id")):
        raise HTTPException(status_code=400, detail="Le json doit contenir l'utilisateur_id et le voyage_id!")

    if not verifier_existence_id(db, models.Utilisateur, "utilisateur_id", infos["utilisateur_id"]):
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas!")
    if not verifier_existence_id(db, models.Voyage, "voyage_id", infos["voyage_id"]):
        raise HTTPException(status_code=404, detail="Ce voyage n'existe pas!")

    return crud.create_relation(db, infos["utilisateur_id"], infos["voyage_id"]).to_dict()


@app.get("/relations", tags=["Relations"])
def get_relations(db: Session = Depends(get_db)):
    """Lister toutes les relations utilisateur-voyage."""
    return [r.to_dict() for r in crud.get_all_relations(db)]


@app.get("/relations/voyage_id/{utilisateur_id}", tags=["Relations"])
def get_voyages_by_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    """Récupérer tous les voyage_id d'un utilisateur."""
    from sqlalchemy import select
    results = db.execute(
        select(models.RelationUtilisateurVoyage.voyage_id).where(
            models.RelationUtilisateurVoyage.utilisateur_id == utilisateur_id
        )
    ).scalars().all()
    if not results:
        raise HTTPException(status_code=404, detail="La relation n'existe pas!")
    return results


@app.get("/relations/utilisateur_id/{voyage_id}", tags=["Relations"])
def get_utilisateurs_by_voyage(voyage_id: int, db: Session = Depends(get_db)):
    """Récupérer tous les utilisateur_id d'un voyage."""
    results = db.execute(
        select(models.RelationUtilisateurVoyage.utilisateur_id).where(
            models.RelationUtilisateurVoyage.voyage_id == voyage_id
        )
    ).scalars().all()
    if not results:
        raise HTTPException(status_code=404, detail="La relation n'existe pas!")
    return results


@app.delete("/relations", tags=["Relations"])
def delete_relation(infos: dict, db: Session = Depends(get_db)):
    """Supprimer une relation utilisateur-voyage."""
    if not all(k in infos for k in ("utilisateur_id", "voyage_id")):
        raise HTTPException(status_code=400, detail="Il faut donner utilisateur_id et voyage_id!")
    deleted = crud.supprimer_relation(db, infos["utilisateur_id"], infos["voyage_id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Cette relation n'existe pas!")
    return {"message": "La relation a bien été supprimée!"}


# =============================================================
# MEMBRE B — DESTINATIONS (One-to-Many avec Voyages)
# =============================================================

@app.post(
    "/voyages/{voyage_id}/destinations/",
    response_model=schemas.DestinationResponse,
    status_code=201,
    tags=["Destinations"],
    summary="Ajouter une étape à un voyage"
)
def ajouter_destination(
    voyage_id: int,
    destination: schemas.DestinationCreate,
    db: Session = Depends(get_db)
):
    """
    Ajoute une étape (hôtel, activité, restaurant) à un voyage existant.

    - **nom** : Nom de la destination — *obligatoire*
    - **localisation** : Ville et/ou pays — *optionnel*
    - **categorie** : `hotel`, `activite` ou `restaurant` — *optionnel*
    - **notes** : Informations complémentaires — *optionnel*
    - **ordre** : Position dans l'itinéraire (>= 1) — *optionnel*
    """
    if not crud.voyage_existe(db, voyage_id):
        raise HTTPException(status_code=404, detail=f"Voyage avec l'id {voyage_id} introuvable.")
    return crud.creer_destination(db=db, destination=destination, voyage_id=voyage_id)


@app.get(
    "/voyages/{voyage_id}/destinations/",
    response_model=List[schemas.DestinationResponse],
    tags=["Destinations"],
    summary="Lister les étapes d'un voyage"
)
def lister_destinations(voyage_id: int, db: Session = Depends(get_db)):
    """Retourne toutes les étapes d'un voyage, triées par ordre croissant."""
    if not crud.voyage_existe(db, voyage_id):
        raise HTTPException(status_code=404, detail=f"Voyage avec l'id {voyage_id} introuvable.")
    return crud.get_destinations_par_voyage(db=db, voyage_id=voyage_id)


@app.get(
    "/destinations/{destination_id}",
    response_model=schemas.DestinationResponse,
    tags=["Destinations"],
    summary="Récupérer le détail d'une étape"
)
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    """Récupère une destination par son ID."""
    destination = crud.get_destination(db=db, destination_id=destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail=f"Destination avec l'id {destination_id} introuvable.")
    return destination


@app.put(
    "/destinations/{destination_id}",
    response_model=schemas.DestinationResponse,
    tags=["Destinations"],
    summary="Modifier une étape"
)
def modifier_destination(
    destination_id: int,
    data: schemas.DestinationUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour partiellement une destination.
    Seuls les champs envoyés sont modifiés, les autres restent inchangés.
    """
    destination = crud.modifier_destination(db=db, destination_id=destination_id, data=data)
    if not destination:
        raise HTTPException(status_code=404, detail=f"Destination avec l'id {destination_id} introuvable.")
    return destination


@app.delete("/destinations/{destination_id}", tags=["Destinations"], summary="Supprimer une étape")
def supprimer_destination(destination_id: int, db: Session = Depends(get_db)):
    """Supprime une destination. Le voyage parent n'est pas affecté."""
    destination = crud.supprimer_destination(db=db, destination_id=destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail=f"Destination avec l'id {destination_id} introuvable.")
    return {"message": f"Destination '{destination.nom}' supprimée avec succès."}


# =============================================================
# MEMBRE C (Zeynab) — BUDGET (One-to-One avec Voyages)
# =============================================================

@app.post(
    "/voyages/{trip_id}/budget",
    response_model=schemas.BudgetResponse,
    status_code=201,
    tags=["Budget"]
)
def create_trip_budget(trip_id: int, budget: schemas.BudgetBase, db: Session = Depends(get_db)):
    """Créer un budget pour un voyage (relation One-to-One)."""
    if not crud.voyage_existe(db, trip_id):
        raise HTTPException(status_code=404, detail="Voyage introuvable.")
    if crud.get_budget_by_trip(db, trip_id):
        raise HTTPException(status_code=400, detail="Ce voyage a déjà un budget.")
    return crud.create_trip_budget(db=db, budget=budget, trip_id=trip_id)


@app.get("/voyages/{trip_id}/budget", tags=["Budget"])
def get_trip_budget(trip_id: int, db: Session = Depends(get_db)):
    """Récupérer le budget d'un voyage."""
    budget = crud.get_budget_by_trip(db=db, trip_id=trip_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget non trouvé pour ce voyage.")
    return budget


@app.put("/voyages/{trip_id}/budget", tags=["Budget"])
def update_trip_budget(trip_id: int, budget_data: schemas.BudgetUpdate, db: Session = Depends(get_db)):
    """Mettre à jour le montant total ou les dépenses effectuées."""
    db_budget = crud.get_budget_by_trip(db=db, trip_id=trip_id)
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget non trouvé.")
    if budget_data.total_amount is not None:
        db_budget.total_amount = budget_data.total_amount
    if budget_data.spent_amount is not None:
        db_budget.spent_amount = budget_data.spent_amount
    db.commit()
    db.refresh(db_budget)
    return db_budget


# =============================================================
# Servir le front-end (doit être DÉCLARÉ APRÈS toutes les routes)
# Le dossier /code/frontend est copié dans l'image Docker.
# =============================================================
import os
FRONTEND_DIR = "/code/frontend"
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
