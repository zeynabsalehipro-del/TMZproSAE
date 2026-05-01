# =============================================================
# schemas_b.py — Partie B : Schémas Pydantic pour les Destinations
# Auteur : Teodora — Membre B
# Projet SAE — Université Sorbonne Paris Nord
#
# Les schémas Pydantic servent à deux choses :
#   1. Valider les données reçues dans les requêtes (corps JSON).
#   2. Définir la structure des données retournées en réponse.
#
# Conventions :
#   - Même style que les schémas de Zeynab (Membre C) dans schemas.py.
#   - Validations inspirées de Verification.py de Mathurin (Membre A).
# =============================================================

from pydantic import BaseModel, field_validator
from typing import Optional

# Catégories autorisées pour une destination
CATEGORIES_VALIDES = {"hotel", "activite", "restaurant"}


# =============================================================
# Schéma pour la création d'une destination
# =============================================================

class DestinationCreate(BaseModel):
    """
    Données attendues lors de la création d'une destination.
    Seul 'nom' est obligatoire. Les autres champs sont optionnels.

    Exemple de corps JSON :
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
        """Le nom ne doit pas être une chaîne vide."""
        if not isinstance(v, str) or v.strip() == "":
            raise ValueError("Le nom ne doit pas être vide!")
        return v.strip()

    @field_validator("categorie")
    @classmethod
    def categorie_valide(cls, v):
        """La catégorie doit être 'hotel', 'activite' ou 'restaurant'."""
        if v is not None and v not in CATEGORIES_VALIDES:
            raise ValueError(
                f"La catégorie doit être l'une des valeurs suivantes : {CATEGORIES_VALIDES}"
            )
        return v

    @field_validator("ordre")
    @classmethod
    def ordre_positif(cls, v):
        """L'ordre doit être un entier positif (>= 1)."""
        if v is not None and v < 1:
            raise ValueError("L'ordre doit être supérieur ou égal à 1!")
        return v


# =============================================================
# Schéma pour la mise à jour partielle d'une destination
# =============================================================

class DestinationUpdate(BaseModel):
    """
    Données pour la mise à jour partielle d'une destination.
    Tous les champs sont optionnels : seuls les champs envoyés seront modifiés.

    Exemple : modifier uniquement les notes :
    {
        "notes": "Annulé, chercher une autre option."
    }
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


# =============================================================
# Schéma pour les réponses API
# =============================================================

class DestinationResponse(BaseModel):
    """
    Structure retournée par l'API pour une destination.
    Cohérent avec BudgetResponse dans schemas.py de Zeynab (Membre C).
    """

    destination_id: int
    nom:            str
    localisation:   Optional[str]
    categorie:      Optional[str]
    notes:          Optional[str]
    ordre:          Optional[int]
    voyage_id:      int

    class Config:
        # Permet à Pydantic de lire les attributs d'un objet SQLAlchemy
        from_attributes = True
