from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, text, Date, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()
class RelationUtilisateurVoyage(Base):
    __tablename__ = "relation_utilisateur_voyage"
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.utilisateur_id", ondelete="CASCADE"), primary_key=True)
    voyage_id = Column(Integer, ForeignKey("voyages.voyage_id", ondelete="CASCADE"), primary_key=True)
    # (optionnel mais recommandé)
    utilisateur = relationship("Utilisateur", back_populates="relations")
    voyage = relationship("Voyage", back_populates="relations")
    def to_dict(self):
        return {
            "utilisateur_id": self.utilisateur_id,
            "voyage_id": self.voyage_id
        }

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    utilisateur_id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    prenom = Column(String(100), nullable=False)
    nom = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    mdp = Column(String(255), nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    __table_args__ = (
        CheckConstraint("age >= 0", name="check_age_positive"),
    )
    relations = relationship(
        "RelationUtilisateurVoyage",
        back_populates="utilisateur",
        passive_deletes=True
    )
    def to_dict(self):
        return {
            "utilisateur_id": self.utilisateur_id,
            "email": self.email,
            "prenom": self.prenom,
            "nom": self.nom,
            "age": self.age,
            "mdp": self.mdp,
            "created_at": self.created_at
        }

class Voyage(Base):
    __tablename__ = "voyages"
    voyage_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    lieu = Column(String(100), nullable=False)
    voyage_fini = Column(Boolean, nullable=False)
    prix = Column(Numeric(10,2), nullable=False)
    __table_args__ = (
        CheckConstraint("prix >= 0", name="check_age_positive"),
    )
    relations = relationship(
        "RelationUtilisateurVoyage",
        back_populates="voyage",
        passive_deletes=True
    )
    def to_dict(self):
        return {
            "voyage_id": self.voyage_id,
            "date": self.date,
            "lieu": self.lieu,
            "voyage_fini": self.voyage_fini,
            "prix": self.prix
        }
