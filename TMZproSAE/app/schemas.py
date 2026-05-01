from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date, datetime


# =============================================================
# MEMBRE C (Zeynab) — Budget schemas
# Repris exactement de schemas.py de Zeynab
# =============================================================

class BudgetBase(BaseModel):
    total_amount: float
    spent_amount: float = 0.0

class BudgetUpdate(BaseModel):
    total_amount: Optional[float] = None
    spent_amount: Optional[float] = None

class BudgetResponse(BudgetBase):
    id:       int
    trip_id:  int

    class Config:
        from_attributes = True


# =============================================================
# MEMBRE B — Destination schemas
# =============================================================

CATEGORIES_VALIDES = {"hotel", "activite", "restaurant"}


class DestinationCreate(BaseModel):
    """
    Données attendues pour créer une destination.
    Seul 'nom' est obligatoire.

    Exemple :
    {
        "nom": "Colisée",
        "localisation": "Rome, Italie",
        "categorie": "activite",
        "notes": "Réserver les billets en avance.",
        "ordre": 1
    }
    """
    nom:          str
    localisation: Optional[str] = None
    categorie:    Optional[str] = None
    notes:        Optional[str] = None
    ordre:        Optional[int] = None

    @field_validator("nom")
    @classmethod
    def nom_non_vide(cls, v):
        if not isinstance(v, str) or v.strip() == "":
            raise ValueError("Le nom ne doit pas être vide!")
        return v.strip()

    @field_validator("categorie")
    @classmethod
    def categorie_valide(cls, v):
        if v is not None and v not in CATEGORIES_VALIDES:
            raise ValueError(
                f"La catégorie doit être l'une des valeurs suivantes : {CATEGORIES_VALIDES}"
            )
        return v

    @field_validator("ordre")
    @classmethod
    def ordre_positif(cls, v):
        if v is not None and v < 1:
            raise ValueError("L'ordre doit être supérieur ou égal à 1!")
        return v


class DestinationUpdate(BaseModel):
    """
    Mise à jour partielle : seuls les champs envoyés sont modifiés.
    """
    nom:          Optional[str] = None
    localisation: Optional[str] = None
    categorie:    Optional[str] = None
    notes:        Optional[str] = None
    ordre:        Optional[int] = None

    @field_validator("nom")
    @classmethod
    def nom_non_vide(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Le nom ne doit pas être vide!")
        return v

    @field_validator("categorie")
    @classmethod
    def categorie_valide(cls, v):
        if v is not None and v not in CATEGORIES_VALIDES:
            raise ValueError(
                f"La catégorie doit être l'une des valeurs suivantes : {CATEGORIES_VALIDES}"
            )
        return v

    @field_validator("ordre")
    @classmethod
    def ordre_positif(cls, v):
        if v is not None and v < 1:
            raise ValueError("L'ordre doit être supérieur ou égal à 1!")
        return v


class DestinationResponse(BaseModel):
    destination_id: int
    nom:            str
    localisation:   Optional[str]
    categorie:      Optional[str]
    notes:          Optional[str]
    ordre:          Optional[int]
    voyage_id:      int

    class Config:
        from_attributes = True
