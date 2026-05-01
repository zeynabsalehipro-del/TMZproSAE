from sqlalchemy import (
    Column, Integer, String, Float, Numeric, Boolean,
    Date, DateTime, ForeignKey, CheckConstraint, text
)
from sqlalchemy.orm import relationship
from .database import Base


# =============================================================
# MEMBRE A (Mathurin) — Utilisateurs, Voyages, Relations
# Structure exacte de Table_Classes.py, portée vers la Base commune
# =============================================================

class RelationUtilisateurVoyage(Base):
    __tablename__ = "relation_utilisateur_voyage"

    utilisateur_id = Column(
        Integer,
        ForeignKey("utilisateurs.utilisateur_id", ondelete="CASCADE"),
        primary_key=True
    )
    voyage_id = Column(
        Integer,
        ForeignKey("voyages.voyage_id", ondelete="CASCADE"),
        primary_key=True
    )
    utilisateur = relationship("Utilisateur", back_populates="relations")
    voyage      = relationship("Voyage",      back_populates="relations")

    def to_dict(self):
        return {
            "utilisateur_id": self.utilisateur_id,
            "voyage_id":      self.voyage_id
        }


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    utilisateur_id = Column(Integer, primary_key=True)
    email          = Column(String(100), nullable=False, unique=True)
    prenom         = Column(String(100), nullable=False)
    nom            = Column(String(100), nullable=False)
    age            = Column(Integer,     nullable=False)
    mdp            = Column(String(255), nullable=False)
    created_at     = Column(DateTime,    nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    __table_args__ = (
        CheckConstraint("age >= 0", name="check_age_positif"),
    )

    relations = relationship(
        "RelationUtilisateurVoyage",
        back_populates="utilisateur",
        passive_deletes=True
    )

    def to_dict(self):
        return {
            "utilisateur_id": self.utilisateur_id,
            "email":          self.email,
            "prenom":         self.prenom,
            "nom":            self.nom,
            "age":            self.age,
            "mdp":            self.mdp,
            "created_at":     str(self.created_at)
        }


class Voyage(Base):
    __tablename__ = "voyages"

    voyage_id   = Column(Integer,      primary_key=True)
    date        = Column(Date,         nullable=False)
    lieu        = Column(String(100),  nullable=False)
    voyage_fini = Column(Boolean,      nullable=False)
    prix        = Column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("prix >= 0", name="check_prix_positif"),
    )

    relations = relationship(
        "RelationUtilisateurVoyage",
        back_populates="voyage",
        passive_deletes=True
    )
    # Relation One-to-Many vers les destinations (Partie B)
    destinations = relationship(
        "Destination",
        back_populates="voyage",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "voyage_id":   self.voyage_id,
            "date":        str(self.date),
            "lieu":        self.lieu,
            "voyage_fini": self.voyage_fini,
            "prix":        float(self.prix)
        }


# =============================================================
# MEMBRE B (Teodora) — Destinations (relation One-to-Many avec Voyage)
# Auteur : Teodora — Membre B
# Un voyage contient plusieurs étapes (hôtel, activité, restaurant).
# =============================================================

class Destination(Base):
    """
    Étape d'un voyage : hôtel, activité ou restaurant.

    Relation One-to-Many :
        voyages (1) ──────< destinations (N)
        voyages.voyage_id ←── destinations.voyage_id

    Si le voyage parent est supprimé, toutes ses destinations
    sont automatiquement supprimées (ON DELETE CASCADE).
    """
    __tablename__ = "destinations"

    destination_id = Column(Integer,      primary_key=True, index=True)
    nom            = Column(String(100),  nullable=False)
    localisation   = Column(String(100),  nullable=True)
    categorie      = Column(String(50),   nullable=True)   # 'hotel', 'activite', 'restaurant'
    notes          = Column(String(255),  nullable=True)
    ordre          = Column(Integer,      nullable=True)   # position dans l'itinéraire

    voyage_id = Column(
        Integer,
        ForeignKey("voyages.voyage_id", ondelete="CASCADE"),
        nullable=False
    )
    voyage = relationship("Voyage", back_populates="destinations")

    __table_args__ = (
        CheckConstraint(
            "categorie IN ('hotel', 'activite', 'restaurant')",
            name="check_categorie_valide"
        ),
    )

    def to_dict(self):
        return {
            "destination_id": self.destination_id,
            "nom":            self.nom,
            "localisation":   self.localisation,
            "categorie":      self.categorie,
            "notes":          self.notes,
            "ordre":          self.ordre,
            "voyage_id":      self.voyage_id,
        }


# =============================================================
# MEMBRE C (Zeynab) — Budget (relation One-to-One avec Voyage)
# Un voyage possède un seul plan budgétaire.
# =============================================================

class Budget(Base):
    __tablename__ = "budgets"

    id           = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float)
    spent_amount = Column(Float, default=0.0)

    # Clé étrangère unique → assure la relation One-to-One
    trip_id = Column(Integer, ForeignKey("voyages.voyage_id"), unique=True)

    def to_dict(self):
        return {
            "id":           self.id,
            "total_amount": self.total_amount,
            "spent_amount": self.spent_amount,
            "trip_id":      self.trip_id
        }
