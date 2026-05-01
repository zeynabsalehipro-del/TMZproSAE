# =============================================================
# crud_b.py — Partie B : Fonctions d'accès à la base de données
# Auteur : Teodora — Membre B
# Projet SAE — Université Sorbonne Paris Nord
#
# Ces fonctions font le lien entre les routes FastAPI (routes_b.py)
# et la base de données PostgreSQL via SQLAlchemy.
#
# Style identique à crud.py de Zeynab (Membre C) :
#   chaque fonction reçoit une session SQLAlchemy (db: Session)
#   et retourne un objet ORM ou None si non trouvé.
# =============================================================

from sqlalchemy.orm import Session
from sqlalchemy import text

from . import models_b, schemas_b


# =============================================================
# Vérification de l'existence d'un voyage
# Inspiré de verifier_existence_id() dans Verification.py de Mathurin
# =============================================================

def voyage_existe(db: Session, voyage_id: int) -> bool:
    """
    Vérifie qu'un voyage existe dans la table 'voyages' de Mathurin.
    Utilise une requête SQL directe pour ne pas créer de dépendance
    vers le modèle Voyage de Mathurin.

    Retourne True si le voyage existe, False sinon.
    """
    result = db.execute(
        text("SELECT voyage_id FROM voyages WHERE voyage_id = :vid"),
        {"vid": voyage_id}
    ).fetchone()
    return result is not None


# =============================================================
# CREATE
# =============================================================

def creer_destination(
    db: Session,
    destination: schemas_b.DestinationCreate,
    voyage_id: int
) -> models_b.Destination:
    """
    Crée une nouvelle destination et l'associe à un voyage existant.

    Args:
        db          : Session SQLAlchemy active.
        destination : Données validées par Pydantic (DestinationCreate).
        voyage_id   : ID du voyage auquel rattacher cette destination.

    Returns:
        L'objet Destination créé, avec son destination_id généré.
    """
    nouvelle_destination = models_b.Destination(
        nom=destination.nom,
        localisation=destination.localisation,
        categorie=destination.categorie,
        notes=destination.notes,
        ordre=destination.ordre,
        voyage_id=voyage_id,
    )
    db.add(nouvelle_destination)
    db.commit()
    db.refresh(nouvelle_destination)
    return nouvelle_destination


# =============================================================
# READ
# =============================================================

def get_destination(db: Session, destination_id: int):
    """
    Récupère une destination par son ID.

    Returns:
        L'objet Destination ou None s'il n'existe pas.
    """
    return (
        db.query(models_b.Destination)
        .filter(models_b.Destination.destination_id == destination_id)
        .first()
    )


def get_destinations_par_voyage(db: Session, voyage_id: int):
    """
    Récupère toutes les destinations d'un voyage,
    triées par ordre croissant (NULL en dernier).

    Returns:
        Liste d'objets Destination (peut être vide).
    """
    return (
        db.query(models_b.Destination)
        .filter(models_b.Destination.voyage_id == voyage_id)
        .order_by(
            models_b.Destination.ordre.is_(None),
            models_b.Destination.ordre.asc()
        )
        .all()
    )


# =============================================================
# UPDATE
# =============================================================

def modifier_destination(
    db: Session,
    destination_id: int,
    data: schemas_b.DestinationUpdate
) -> models_b.Destination:
    """
    Met à jour partiellement une destination.
    Seuls les champs présents dans la requête sont modifiés.
    Inspiré de modify_from_arg() dans Petites_Methodes.py de Mathurin.

    Returns:
        L'objet Destination mis à jour, ou None s'il n'existe pas.
    """
    destination = get_destination(db, destination_id)
    if not destination:
        return None

    for champ, valeur in data.model_dump(exclude_unset=True).items():
        setattr(destination, champ, valeur)

    db.commit()
    db.refresh(destination)
    return destination


# =============================================================
# DELETE
# =============================================================

def supprimer_destination(db: Session, destination_id: int) -> models_b.Destination:
    """
    Supprime une destination par son ID.
    Le voyage parent n'est pas affecté.
    Inspiré de delete_from_arg() dans Petites_Methodes.py de Mathurin.

    Returns:
        L'objet Destination supprimé (pour confirmation), ou None s'il n'existe pas.
    """
    destination = get_destination(db, destination_id)
    if not destination:
        return None

    db.delete(destination)
    db.commit()
    return destination
