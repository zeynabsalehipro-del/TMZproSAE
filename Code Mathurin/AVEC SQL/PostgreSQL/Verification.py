import re
from src.PostgreSQL.db_PostgreSQL import get_connection
from sqlalchemy import select
from src.PostgreSQL.Table_Classes import Utilisateur
import calendar
def verifier_str(info, nom):
    if not isinstance(info, str):
        return f"Un {nom} doit être un String!"
    else:
        if info=="":
            return "La valeur ne doit pas être vide!"
    return "OK"

def verifier_int(info, nom):
    if not isinstance(info, int):
        return f"Un {nom} doit être un Integer!"
    else:
        if info=="":
            return "La valeur ne doit pas être vide!"
    return "OK"

def verifier_email(email):
    message=verifier_str(email,"email")
    if message!="OK":
        return message
    else :
        if re.search(r".+@.+\..+", email) is None:
            return "L'email doit être de la forme x@y.z!"
    return "OK"

def verifier_existence_email(email):
    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    session.close()
    if not result:
        return False
    else:
        return True

def verifier_date(jour, mois, annee):
    if mois not in range(1,12+1):
        return "Mois dois être entre 1 et 12!"
    else:
        if mois in range(1,7+1,2) or mois in range(8,12+1,2):
            if jour not in range(1,31+1):
                return "Jour dois être entre 1 et 31!"
        else:
            if mois in range(4,6+1,2) or mois in range(9,11+1,2):
                if jour not in range(1,30+1):
                    return "Jour dois être entre 1 et 30!"
            else: #donc que mois=2
                if calendar.isleap(annee): #Si année bissextile
                    if jour not in range(1,29+1):
                        return "Jour dois être entre 1 et 29!"
                else: #Si année pas bissextile
                    if jour not in range(1,28+1):
                        return "Jour dois être entre 1 et 28!"
    return "OK"

def verifier_existence_id(table, variable, id):
    session = get_connection()
    stmt = select(table).where(getattr(table, variable) == id)
    result = session.execute(stmt).scalars().first()
    session.close()
    if not result:
        return False
    else:
        return True

def verification_utilisateur(cle, info):
    if cle=="email":
        message=verifier_email(info)
        if message!="OK":
            return message
        verif=verifier_existence_email(info)
        if verif==True: #Donc que l'email existe
            return "L'email existe déja!"
    else:
        if cle=="prenom":
            message=verifier_str(info,cle)
            if message!="OK":
                return message
        else:
            if cle=="prenom":
                message=verifier_str(info,cle)
                if message!="OK":
                    return message
            else:
                if cle=="age":
                    if info<0:
                        return "L'âge doit être supérieur ou égale a 0!"
                else: #Donc que cle=="mdp"
                    message=verifier_str(info,cle)
                    if message!="OK":
                        return message
    return "OK"

def verification_voyage(cle, info):
    if cle=="prix":
        if info<0:
            return "Un prix ne peut pas être négatif!"
    else:
        if cle=="voyage_fini":
            if not isinstance(info, bool):
                return "La valeur doit être un Boolean!"
        else: #Donc que clé=="lieu"
            return verifier_str(info,"lieu")
    return "OK"
