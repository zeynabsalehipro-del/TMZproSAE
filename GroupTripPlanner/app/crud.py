# =============================================================
# crud.py — Fonctions d'accès à la base de données
#
# Regroupe :
#   - Les fonctions de Zeynab (Membre C) : Budget
#   - Les fonctions de Mathurin (Membre A) : portées en SQLAlchemy ORM
#   - Les fonctions de la Partie B        : Destinations
# =============================================================

from sqlalchemy.orm import Session
from sqlalchemy import select, func, text
from datetime import date as date_type

from . import models, schemas


# =============================================================
# MEMBRE C (Zeynab) — Budget
# Repris exactement de crud.py de Zeynab
# =============================================================

def get_budget_by_trip(db: Session, trip_id: int):
    return db.query(models.Budget).filter(models.Budget.trip_id == trip_id).first()


def create_trip_budget(db: Session, budget: schemas.BudgetBase, trip_id: int):
    db_budget = models.Budget(**budget.dict(), trip_id=trip_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


# =============================================================
# MEMBRE A (Mathurin) — Utilisateurs
# Portage de Petites_Methodes.py vers des fonctions avec session injectée
# =============================================================

def get_all_utilisateurs(db: Session):
    return db.execute(select(models.Utilisateur)).scalars().all()


def get_utilisateur_by_email(db: Session, email: str):
    return db.execute(
        select(models.Utilisateur).where(models.Utilisateur.email == email)
    ).scalars().first()


def create_utilisateur(db: Session, infos: dict):
    nouvel_utilisateur = models.Utilisateur(
        email=infos["email"],
        prenom=infos["prenom"],
        nom=infos["nom"],
        age=infos["age"],
        mdp=infos["mdp"]
    )
    db.add(nouvel_utilisateur)
    db.commit()
    db.refresh(nouvel_utilisateur)
    return nouvel_utilisateur


def modifier_utilisateur(db: Session, email: str, champ: str, valeur):
    utilisateur = get_utilisateur_by_email(db, email)
    if not utilisateur:
        return None
    setattr(utilisateur, champ, valeur)
    db.commit()
    db.refresh(utilisateur)
    return utilisateur


def supprimer_utilisateur(db: Session, email: str):
    utilisateur = get_utilisateur_by_email(db, email)
    if not utilisateur:
        return None
    db.delete(utilisateur)
    db.commit()
    return utilisateur


# =============================================================
# MEMBRE A (Mathurin) — Voyages
# =============================================================

def get_all_voyages(db: Session):
    return db.execute(select(models.Voyage)).scalars().all()


def get_voyage_by_id(db: Session, voyage_id: int):
    return db.execute(
        select(models.Voyage).where(models.Voyage.voyage_id == voyage_id)
    ).scalars().first()


def create_voyage(db: Session, infos: dict):
    nouveau_voyage = models.Voyage(
        date=date_type(infos["annee"], infos["mois"], infos["jour"]),
        lieu=infos["lieu"],
        voyage_fini=False,
        prix=infos["prix"]
    )
    db.add(nouveau_voyage)
    db.commit()
    db.refresh(nouveau_voyage)
    return nouveau_voyage


def modifier_voyage(db: Session, voyage_id: int, champ: str, valeur):
    voyage = get_voyage_by_id(db, voyage_id)
    if not voyage:
        return None
    setattr(voyage, champ, valeur)
    db.commit()
    db.refresh(voyage)
    return voyage


def supprimer_voyage(db: Session, voyage_id: int):
    voyage = get_voyage_by_id(db, voyage_id)
    if not voyage:
        return None
    db.delete(voyage)
    db.commit()
    return voyage


# =============================================================
# MEMBRE A (Mathurin) — Relations Utilisateur <-> Voyage
# =============================================================

def get_all_relations(db: Session):
    return db.execute(select(models.RelationUtilisateurVoyage)).scalars().all()


def get_relation(db: Session, utilisateur_id: int, voyage_id: int):
    return db.execute(
        select(models.RelationUtilisateurVoyage).where(
            models.RelationUtilisateurVoyage.utilisateur_id == utilisateur_id,
            models.RelationUtilisateurVoyage.voyage_id == voyage_id,
        )
    ).scalars().first()


def create_relation(db: Session, utilisateur_id: int, voyage_id: int):
    nouvelle_relation = models.RelationUtilisateurVoyage(
        utilisateur_id=utilisateur_id,
        voyage_id=voyage_id
    )
    db.add(nouvelle_relation)
    db.commit()
    db.refresh(nouvelle_relation)
    return nouvelle_relation


def supprimer_relation(db: Session, utilisateur_id: int, voyage_id: int):
    relation = get_relation(db, utilisateur_id, voyage_id)
    if not relation:
        return None
    db.delete(relation)
    db.commit()
    return relation


# =============================================================
# MEMBRE B (Teodora) — Destinations
# =============================================================

def voyage_existe(db: Session, voyage_id: int) -> bool:
    """Vérifie qu'un voyage existe dans la table 'voyages'."""
    result = db.execute(
        text("SELECT voyage_id FROM voyages WHERE voyage_id = :vid"),
        {"vid": voyage_id}
    ).fetchone()
    return result is not None


def get_destination(db: Session, destination_id: int):
    """Récupère une destination par son ID."""
    return (
        db.query(models.Destination)
        .filter(models.Destination.destination_id == destination_id)
        .first()
    )


def get_destinations_par_voyage(db: Session, voyage_id: int):
    """Récupère toutes les destinations d'un voyage, triées par ordre croissant."""
    return (
        db.query(models.Destination)
        .filter(models.Destination.voyage_id == voyage_id)
        .order_by(
            models.Destination.ordre.is_(None),
            models.Destination.ordre.asc()
        )
        .all()
    )


def creer_destination(db: Session, destination: schemas.DestinationCreate, voyage_id: int):
    """Crée une nouvelle destination liée à un voyage existant."""
    nouvelle_destination = models.Destination(
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


def modifier_destination(db: Session, destination_id: int, data: schemas.DestinationUpdate):
    """Met à jour partiellement une destination (seuls les champs envoyés changent)."""
    destination = get_destination(db, destination_id)
    if not destination:
        return None
    for champ, valeur in data.model_dump(exclude_unset=True).items():
        setattr(destination, champ, valeur)
    db.commit()
    db.refresh(destination)
    return destination


def supprimer_destination(db: Session, destination_id: int):
    """Supprime une destination. Le voyage parent n'est pas affecté."""
    destination = get_destination(db, destination_id)
    if not destination:
        return None
    db.delete(destination)
    db.commit()
    return destination
