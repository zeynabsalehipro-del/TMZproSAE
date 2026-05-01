# =============================================================
# models_b.py — Partie B : Modèle SQLAlchemy pour les Destinations
# Auteur : Teodora — Membre B
# Projet SAE — Université Sorbonne Paris Nord
#
# Ce fichier définit la table 'destinations' dans la base de données.
# Elle est liée à la table 'voyages' de Mathurin (Membre A) via une
# relation One-to-Many :
#     → Un voyage peut contenir plusieurs destinations (étapes).
#     → Une destination appartient à exactement un voyage.
#
# Pour intégrer : importer ce modèle dans models.py du projet commun
# et s'assurer que Base.metadata.create_all() est appelé après cet import.
# =============================================================

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

# Base commune au projet (définie dans database.py)
from .database import Base


class Destination(Base):
    """
    Représente une étape d'un voyage : hôtel, activité ou restaurant.

    Relation One-to-Many avec la table 'voyages' (Mathurin — Membre A) :
        Voyage (1) ──────< Destination (N)
        voyages.voyage_id ←── destinations.voyage_id

    Si le voyage parent est supprimé, toutes ses destinations sont
    automatiquement supprimées (ON DELETE CASCADE).

    Attributs :
        destination_id : Identifiant unique auto-incrémenté.
        nom            : Nom de l'étape (ex: "Colisée", "Hôtel Ibis").
        localisation   : Ville et/ou pays (ex: "Rome, Italie").
        categorie      : Type d'étape : 'hotel', 'activite' ou 'restaurant'.
        notes          : Informations complémentaires libres.
        ordre          : Position de l'étape dans l'itinéraire (1, 2, 3...).
        voyage_id      : Clé étrangère vers le voyage parent.
    """

    __tablename__ = "destinations"

    destination_id = Column(Integer, primary_key=True, index=True)

    nom = Column(
        String(100),
        nullable=False,
        comment="Nom de la destination, ex: 'Colisée', 'Hôtel Ibis'"
    )
    localisation = Column(
        String(100),
        nullable=True,
        comment="Ville et/ou pays, ex: 'Rome, Italie'"
    )
    categorie = Column(
        String(50),
        nullable=True,
        comment="Type d'étape : 'hotel', 'activite' ou 'restaurant'"
    )
    notes = Column(
        String(255),
        nullable=True,
        comment="Informations complémentaires libres"
    )
    ordre = Column(
        Integer,
        nullable=True,
        comment="Position dans l'itinéraire (1 = première étape)"
    )

    # ----------------------------------------------------------
    # Clé étrangère vers la table 'voyages' de Mathurin (Membre A)
    # ON DELETE CASCADE : si le voyage est supprimé, toutes ses
    # destinations sont automatiquement supprimées aussi.
    # ----------------------------------------------------------
    voyage_id = Column(
        Integer,
        ForeignKey("voyages.voyage_id", ondelete="CASCADE"),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "categorie IN ('hotel', 'activite', 'restaurant')",
            name="check_categorie_valide"
        ),
    )

    def to_dict(self):
        """Convertit l'objet en dictionnaire — cohérent avec les to_dict() de Mathurin."""
        return {
            "destination_id": self.destination_id,
            "nom":            self.nom,
            "localisation":   self.localisation,
            "categorie":      self.categorie,
            "notes":          self.notes,
            "ordre":          self.ordre,
            "voyage_id":      self.voyage_id,
        }
