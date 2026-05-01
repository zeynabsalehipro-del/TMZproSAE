# =============================================================
# verification.py — Fonctions de validation
# Portage de Verification.py de Mathurin (Membre A)
# Adapté pour fonctionner avec la session SQLAlchemy partagée
# =============================================================

import re
import calendar
from sqlalchemy.orm import Session
from sqlalchemy import select


def verifier_str(info, nom: str) -> str:
    if not isinstance(info, str):
        return f"Un {nom} doit être un String!"
    if info == "":
        return "La valeur ne doit pas être vide!"
    return "OK"


def verifier_int(info, nom: str) -> str:
    if not isinstance(info, int):
        return f"Un {nom} doit être un Integer!"
    return "OK"


def verifier_email(email) -> str:
    message = verifier_str(email, "email")
    if message != "OK":
        return message
    if re.search(r".+@.+\..+", email) is None:
        return "L'email doit être de la forme x@y.z!"
    return "OK"


def verifier_existence_email(db: Session, email: str) -> bool:
    from .models import Utilisateur
    stmt   = select(Utilisateur).where(Utilisateur.email == email)
    result = db.execute(stmt).scalars().first()
    return result is not None


def verifier_date(jour: int, mois: int, annee: int) -> str:
    if mois not in range(1, 13):
        return "Mois doit être entre 1 et 12!"
    if mois in range(1, 8, 2) or mois in range(8, 13, 2):
        if jour not in range(1, 32):
            return "Jour doit être entre 1 et 31!"
    elif mois in range(4, 7, 2) or mois in range(9, 12, 2):
        if jour not in range(1, 31):
            return "Jour doit être entre 1 et 30!"
    else:  # mois == 2
        max_jour = 29 if calendar.isleap(annee) else 28
        if jour not in range(1, max_jour + 1):
            return f"Jour doit être entre 1 et {max_jour}!"
    return "OK"


def verifier_existence_id(db: Session, table, champ: str, valeur) -> bool:
    stmt   = select(table).where(getattr(table, champ) == valeur)
    result = db.execute(stmt).scalars().first()
    return result is not None


def verification_utilisateur(cle: str, info) -> str:
    if cle == "email":
        return verifier_email(info)
    if cle in ("prenom", "nom", "mdp"):
        return verifier_str(info, cle)
    if cle == "age":
        if info < 0:
            return "L'âge doit être supérieur ou égal à 0!"
    return "OK"


def verification_voyage(cle: str, info) -> str:
    if cle == "prix":
        if info < 0:
            return "Un prix ne peut pas être négatif!"
    elif cle == "voyage_fini":
        if not isinstance(info, bool):
            return "La valeur doit être un Boolean!"
    elif cle == "lieu":
        return verifier_str(info, "lieu")
    return "OK"
