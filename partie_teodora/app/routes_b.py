# =============================================================
# routes_b.py — Partie B : Routes FastAPI pour les Destinations
# Auteur : Teodora — Membre B
# Projet SAE — Université Sorbonne Paris Nord
#
# Ce fichier définit un APIRouter FastAPI qui expose toutes les
# routes pour la gestion des destinations (étapes d'un voyage).
#
# Relation implémentée : One-to-Many
#     voyages (1) ──────< destinations (N)
#
# Pour intégrer dans main.py du projet commun, ajouter :
#     from app.routes_b import router as router_destinations
#     app.include_router(router_destinations)
#
# Routes exposées :
#     POST   /voyages/{voyage_id}/destinations/  → Ajouter une étape
#     GET    /voyages/{voyage_id}/destinations/  → Lister les étapes
#     GET    /destinations/{destination_id}      → Détail d'une étape
#     PUT    /destinations/{destination_id}      → Modifier une étape
#     DELETE /destinations/{destination_id}      → Supprimer une étape
# =============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud_b, schemas_b
from .database import SessionLocal

router = APIRouter()


def get_db():
    """Crée et ferme une session SQLAlchemy par requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================================================
# POST — Ajouter une destination à un voyage
# =============================================================

@router.post(
    "/voyages/{voyage_id}/destinations/",
    response_model=schemas_b.DestinationResponse,
    status_code=201,
    tags=["Gestion des Destinations"],
    summary="Ajouter une étape à un voyage",
)
def ajouter_destination(
    voyage_id: int,
    destination: schemas_b.DestinationCreate,
    db: Session = Depends(get_db),
):
    """
    Ajoute une nouvelle étape (destination) à un voyage existant.

    - **voyage_id** : ID du voyage (doit exister dans la table 'voyages').
    - **nom** : Nom de la destination — *obligatoire*.
    - **localisation** : Ville et/ou pays — *optionnel*.
    - **categorie** : `hotel`, `activite` ou `restaurant` — *optionnel*.
    - **notes** : Informations complémentaires — *optionnel*.
    - **ordre** : Position dans l'itinéraire (>= 1) — *optionnel*.

    Retourne la destination créée avec son `destination_id`.
    """
    if not crud_b.voyage_existe(db, voyage_id):
        raise HTTPException(
            status_code=404,
            detail=f"Voyage avec l'id {voyage_id} introuvable."
        )
    return crud_b.creer_destination(db=db, destination=destination, voyage_id=voyage_id)


# =============================================================
# GET — Lister toutes les destinations d'un voyage
# =============================================================

@router.get(
    "/voyages/{voyage_id}/destinations/",
    response_model=List[schemas_b.DestinationResponse],
    tags=["Gestion des Destinations"],
    summary="Lister les étapes d'un voyage",
)
def lister_destinations(voyage_id: int, db: Session = Depends(get_db)):
    """
    Retourne toutes les étapes d'un voyage, triées par ordre croissant.
    Retourne une liste vide [] si le voyage n'a pas encore de destinations.
    """
    if not crud_b.voyage_existe(db, voyage_id):
        raise HTTPException(
            status_code=404,
            detail=f"Voyage avec l'id {voyage_id} introuvable."
        )
    return crud_b.get_destinations_par_voyage(db=db, voyage_id=voyage_id)


# =============================================================
# GET — Détail d'une destination spécifique
# =============================================================

@router.get(
    "/destinations/{destination_id}",
    response_model=schemas_b.DestinationResponse,
    tags=["Gestion des Destinations"],
    summary="Récupérer le détail d'une étape",
)
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    """Retourne le détail d'une destination par son destination_id."""
    destination = crud_b.get_destination(db=db, destination_id=destination_id)
    if not destination:
        raise HTTPException(
            status_code=404,
            detail=f"Destination avec l'id {destination_id} introuvable."
        )
    return destination


# =============================================================
# PUT — Modifier une destination (mise à jour partielle)
# =============================================================

@router.put(
    "/destinations/{destination_id}",
    response_model=schemas_b.DestinationResponse,
    tags=["Gestion des Destinations"],
    summary="Modifier une étape",
)
def modifier_destination(
    destination_id: int,
    data: schemas_b.DestinationUpdate,
    db: Session = Depends(get_db),
):
    """
    Met à jour partiellement une destination existante.
    Seuls les champs présents dans le corps sont modifiés.

    Exemple : modifier uniquement les notes :
    ```json
    { "notes": "Réservation annulée, trouver une alternative." }
    ```
    """
    destination = crud_b.modifier_destination(db=db, destination_id=destination_id, data=data)
    if not destination:
        raise HTTPException(
            status_code=404,
            detail=f"Destination avec l'id {destination_id} introuvable."
        )
    return destination


# =============================================================
# DELETE — Supprimer une destination
# =============================================================

@router.delete(
    "/destinations/{destination_id}",
    tags=["Gestion des Destinations"],
    summary="Supprimer une étape",
)
def supprimer_destination(destination_id: int, db: Session = Depends(get_db)):
    """
    Supprime une destination par son destination_id.
    Le voyage parent n'est pas affecté.
    Les autres destinations du même voyage restent inchangées.
    """
    destination = crud_b.supprimer_destination(db=db, destination_id=destination_id)
    if not destination:
        raise HTTPException(
            status_code=404,
            detail=f"Destination avec l'id {destination_id} introuvable."
        )
    return {
        "message": f"Destination '{destination.nom}' (id={destination_id}) supprimée avec succès."
    }
