from db_PostgreSQL import get_connection
from sqlalchemy import select
from Table_Classes import *

def select_from_arg(champ_retour, table, champ, valeur):
    session = get_connection()
    if champ_retour=="*":
        stmt = select(table).where(getattr(table, champ) == valeur)
    else:
        stmt = select(getattr(table, champ_retour)).where(getattr(table, champ) == valeur)
    result = session.execute(stmt).scalars().all()
    return result

def modify_from_arg(table, valeur_reconnaissance, champ, nouvelle_valeur):
    session = get_connection()
    if table==Utilisateur:
        stmt = select(Utilisateur.utilisateur_id).where(Utilisateur.email == valeur_reconnaissance)
        id = session.execute(stmt).scalars().first()
        a_modifier = session.get(table, id)
    else:
        a_modifier = session.get(table, valeur_reconnaissance)
    setattr(a_modifier, champ, nouvelle_valeur)
    session.commit()
    session.close()

def delete_from_arg(table, valeur_reconnaissance):
    session = get_connection()
    if table==Utilisateur:
        stmt = select(Utilisateur.utilisateur_id).where(Utilisateur.email == valeur_reconnaissance)
        id = session.execute(stmt).scalars().first()
        a_effacer = session.get(table, id)
    else:
        a_effacer = session.get(table, valeur_reconnaissance)
    session.delete(a_effacer)
    session.commit()
    session.close()
