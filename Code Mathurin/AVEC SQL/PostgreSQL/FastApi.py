from Verification import *
from Table_Classes import *
from src.PostgreSQL.Petites_Methodes import *
from datetime import date
from fastapi import FastAPI, HTTPException

app=FastAPI()

@app.get('/')
def home():
    return ("Bienvenue dans l'API de gestion des utilisateurs! \n"
            "Voici les variables/colonnes utiles pour les différentes classes/tables:\n"
            "Utilisateurs: utilisateur_id, email (de la forme x@y.z), prenom, nom, age et mdp.\n"
            "Voyages: jour, mois et annee (seront combiné dans une seule variable/colonne nommé date, lieu, voyage_fini (True ou False) et prix\n"
            "Relations_Utilisateur_Voyage: utilisateur_id et voyage_id")

@app.post('/utilisateurs')
def post_utilisateur(infos: dict):
    #Vérifier qu'infos contient bien toutes les infos

    if not ("email" in infos and "prenom" in infos and "nom" in infos and "age" in infos and "mdp" in infos):
        raise HTTPException(status_code=404, detail="Le json doit contenir l'email, le prénom, le nom, l'âge et le mot de passe!")
    message=verifier_email(infos['email'])
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)
    verif=verifier_existence_email(infos['email'])
    if verif==True: #Donc que l'email existe
        return HTTPException(status_code=404, detail="L'email existe déja!")

    message=verifier_str(infos['prenom'],"prenom")
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    message=verifier_str(infos['nom'],"nom")
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    if not isinstance(infos['age'], int):
        return HTTPException(status_code=404, detail="Un age doit être un Integer!")
    if infos['age']<0:
        return HTTPException(status_code=404, detail="L'âge doit être supérieur ou égale a 0!")

    message=verifier_str(infos['mdp'],"mdp")
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    session = get_connection()
    nouvel_utilisateur = Utilisateur(
        email=infos['email'],
        prenom=infos['prenom'],
        nom=infos['nom'],
        age=infos['age'],
        mdp=infos['mdp']
    )
    session.add(nouvel_utilisateur)
    session.commit()
    stmt = select(Utilisateur).where(Utilisateur.email == infos['email'])
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()
    #Le code 201 pour dire création réussie

@app.post('/voyages')
def post_voyage(infos: dict):
    if not ("jour" in infos and "mois" in infos and "annee" in infos and "lieu" in infos and "prix" in infos):
        return HTTPException(status_code=404, detail="Le json doit contenir le jour, le mois, l'année, le lieu, l'état du voyage (fini ou non/True ou False) et le prix!")

    message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    message=verifier_str(infos['lieu'],"lieu")
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    if not isinstance(infos['prix'], int) and not isinstance(infos['prix'], float) :
        raise HTTPException(status_code=404, detail="Un prix doit être un Integer ou un Float!")
    if infos['prix']<0:
        raise HTTPException(status_code=404, detail="Un prix ne peut pas être négatif!")

    session = get_connection()
    nouveau_voyage = Voyage(
        date=date(infos['annee'], infos['mois'], infos['jour']),
        lieu=infos['lieu'],
        voyage_fini=False,
        prix=infos['prix']
    )
    session.add(nouveau_voyage)
    session.commit()
    stmt = select(func.max(Voyage.voyage_id))
    result = session.execute(stmt).scalar()
    stmt = select(Voyage).where(Voyage.voyage_id == result)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()
    #Le code 201 pour dire création réussie

@app.post('/relations')
def post_relation(infos: dict):
    if not("utilisateur_id" in infos and "voyage_id" in infos):
        raise HTTPException(status_code=404, detail="Le json doit contenir l'id du participant et l'id du voyage!")
    verif=verifier_existence_id(Utilisateur, "utilisateur_id", infos['utilisateur_id'])
    if verif==False: #Donc que l'email n'existe pas
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas!")
    verif=verifier_existence_id(Voyage, "voyage_id", infos['voyage_id'])
    if verif==False: #Donc que le voyage n'existe pas
        raise HTTPException(status_code=404, detail="Ce voyage n'existe pas!")
    #Pas besoin de plus de vérification. Comme les emails et les ids doivent être préexistants ca veut dire qu'ils ont passé les checks.

    session = get_connection()
    nouvelle_relation = RelationUtilisateurVoyage(
        utilisateur_id=infos['utilisateur_id'],
        voyage_id=infos['voyage_id']
    )
    session.add(nouvelle_relation)
    session.commit()
    stmt = select(RelationUtilisateurVoyage).where(
        RelationUtilisateurVoyage.utilisateur_id == infos['utilisateur_id'],
        RelationUtilisateurVoyage.voyage_id == infos['voyage_id'],
    )
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()
    #Le code 201 pour dire création réussie

#Partie Get
@app.get('/utilisateurs')
#Méthode HTTP GET qui permet de retourner la liste des utilisateurs
def get_utilisateurs():
    #jsonify transforme result en json
    session = get_connection()
    stmt = select(Utilisateur)
    result = session.execute(stmt).scalars().all()
    for u in result:
        print(u.to_dict())
    session.close()
    return [u.to_dict() for u in result]

@app.get('/utilisateurs/nom/<string:email>')
#On peut tester avec http://127.0.0.1:5000/utilisateurs/mdp/Test@test.com par exemple
def get_nom_by_email(email):
    result=select_from_arg("nom", Utilisateur, "email", email)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas !")
    else :
        return [u for u in result]

@app.get('/utilisateurs/prenom/<string:email>')
def get_prenom_by_email(email):
    result=select_from_arg("prenom", Utilisateur, "email", email)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas !")
    else :
        return [u for u in result]

@app.get('/utilisateurs/age/<string:email>')
def get_age_by_email(email):
    result=select_from_arg("age", Utilisateur, "email", email)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas !")
    else :
        return [u for u in result]

@app.get('/utilisateurs/mdp/<string:email>')
def get_mdp_by_email(email):
    result=select_from_arg("mdp", Utilisateur, "email", email)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas !")
    else :
        return [u for u in result]

@app.get('/utilisateurs/all/<string:email>')
def get_all_by_email(email):
    result=select_from_arg("*", Utilisateur, "email", email)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas !")
    else :
        return [u.to_dict() for u in result]


@app.get('/voyages')
#Méthode HTTP GET qui permet de retourner la liste des utilisateurs
def get_voyages():
    session = get_connection()
    stmt = select(Voyage)
    result = session.execute(stmt).scalars().all()
    for u in result:
        print(u.to_dict())
    session.close()
    return [u.to_dict() for u in result]

@app.get('/voyages/date/<int:voyage_id>')
def get_date_by_voyage_id(voyage_id):
    result=select_from_arg("date", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas !")
    else :
        return [u for u in result]

@app.get('/voyages/lieu/<int:voyage_id>')
def get_lieu_by_voyage_id(voyage_id):
    result=select_from_arg("lieu", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas !")
    else :
        return [u for u in result]

@app.get('/voyages/voyage_fini/<int:voyage_id>')
def get_voyage_fini_by_voyage_id(voyage_id):
    result=select_from_arg("voyage_fini", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas !")
    else :
        return [u for u in result]

@app.get('/voyages/prix/<int:voyage_id>')
def get_prix_by_voyage_id(voyage_id):
    result=select_from_arg("prix", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas !")
    else :
        return [u for u in result]

@app.get('/voyages/all/<int:voyage_id>')
def get_all_voyages_by_voyage_id(voyage_id):
    result=select_from_arg("*", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas !")
    else :
        return [u.to_dict() for u in result]


@app.get('/relations')
def get_relations():
    session = get_connection()
    stmt = select(RelationUtilisateurVoyage)
    result = session.execute(stmt).scalars().all()
    for u in result:
        print(u.to_dict())
    session.close()
    return [u.to_dict() for u in result]

@app.get('/relations/voyage_id/<int:utilisateur_id>')
#Vous donnez l'id de l'utilisateur ca sort les id de tous les voyages qu'il a fait
def get_voyage_id_by_email(utilisateur_id):
    result=select_from_arg("voyage_id", RelationUtilisateurVoyage, "utilisateur_id", utilisateur_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="La relation n'existe pas !")
    else :
        return [u for u in result]

@app.get('/relations/utilisateur_id/<int:voyage_id>')
def get_email_by_voyage_id(voyage_id):
    result=select_from_arg("utilisateur_id", RelationUtilisateurVoyage, "voyage_id", voyage_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="La relation n'existe pas !")
    else :
        return [u for u in result]

#Les deux méthodes précedentes et les deux suivantes servent a la même chose mais je les ai quand même mis. On sait jamais.

@app.get('/relations/all/utilisateur_id/<int:utilisateur_id>')
def get_all_by_utilisateur_id(utilisateur_id):
    result=select_from_arg("*", RelationUtilisateurVoyage, "utilisateur_id", utilisateur_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="L'email n'est dans pas dans la table!")
    else :
        return [u.to_dict() for u in result]

@app.get('/relations/all/voyage_id/<int:voyage_id>')
def get_all_relations_by_voyage_id(voyage_id):
    result=select_from_arg("*", RelationUtilisateurVoyage, "voyage_id", voyage_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="L'id n'est dans pas dans la table!")
    else :
        return [u.to_dict() for u in result]

@app.get('/relations/one_line')
def get_one_line_relations(infos: dict):
    if "utilisateur_id" in infos and "voyage_id" in infos:
        session = get_connection()
        stmt = select(RelationUtilisateurVoyage).where(
            RelationUtilisateurVoyage.utilisateur_id == infos["utilisateur_id"],
            RelationUtilisateurVoyage.voyage_id == infos["voyage_id"]
        )
        result = session.execute(stmt).scalars().first()
        session.close()
        if not result:
            raise HTTPException(status_code=404, detail="Cette relation n'existe pas!")
        else :
            return result.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Il faut donner 2 arguments : utilisateur_id et voyage_id!")


#Partie Patch
@app.patch('/utilisateurs/email/<string:email>')
def patch_email(email, infos: dict):
    #Rajouter un garde fou, le nouvel email ne doit pas exister
    if not "email" in infos:
        raise HTTPException(status_code=404, detail="Le json doit contenir l'email!")
    message=verifier_email(infos['email'])
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)
    verif=verifier_existence_email(infos['email'])
    if verif==True: #Donc que l'email existe
        raise HTTPException(status_code=404, detail="L'email existe déja!")

    modify_from_arg(Utilisateur, email, "email", infos['email'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == infos['email'])
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()

@app.route('/utilisateurs/prenom/<string:email>', methods=['PATCH'])
def patch_prenom(email, infos: dict):
    if not "prenom" in infos:
        raise HTTPException(status_code=404, detail="Le json doit contenir le prénom!")
    message=verifier_str(infos['prenom'],"prénom")
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    modify_from_arg(Utilisateur, email, "prenom", infos['prenom'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()

@app.patch('/utilisateurs/nom/<string:email>')
def patch_nom(email, infos: dict):
    if not "nom" in infos:
        raise HTTPException(status_code=404, detail="Le json doit contenir le nom!")
    message=verifier_str(infos['nom'],"nom")
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    modify_from_arg(Utilisateur, email, "nom", infos['nom'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()

@app.patch('/utilisateurs/age/<string:email>')
def patch_age(email, infos: dict):
    if not "age" in infos:
        raise HTTPException(status_code=404, detail="Le json doit contenir l'âge!")
    if infos['age']<0:
        raise HTTPException(status_code=404, detail="L'âge doit être supérieur ou égale a 0!")

    modify_from_arg(Utilisateur, email, "age", infos['age'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()

@app.patch('/utilisateurs/mdp/<string:email>')
def patch_mdp(email, infos: dict):
    if not "mdp" in infos:
        raise HTTPException(status_code=404, detail="Le json doit contenir le mot de passe!")
    message=verifier_str(infos['mdp'],"mdp")
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    modify_from_arg(Utilisateur, email, "mdp", infos['mdp'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()


@app.patch('/voyages/date/<int:voyage_id>')
def patch_date(voyage_id, infos: dict):
    if not ("jour" in infos and "mois" in infos and "annee" in infos):
        raise HTTPException(status_code=404, detail="Le json doit contenir le jour, le mois et l'année!")
    message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    modify_from_arg(Voyage, voyage_id, "date", date(infos['annee'], infos['mois'], infos['jour']))

    session = get_connection()
    stmt = select(Voyage).where(Voyage.voyage_id == voyage_id)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()

@app.patch('/voyages/lieu/<int:voyage_id>')
def patch_lieu(voyage_id, infos: dict):
    if not "lieu" in infos:
        raise HTTPException(status_code=404, detail="Le json doit contenir le lieu!")
    message=verifier_str(infos['lieu'],"lieu")
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)

    modify_from_arg(Voyage, voyage_id, "lieu", infos['lieu'])

    session = get_connection()
    stmt = select(Voyage).where(Voyage.voyage_id == voyage_id)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()

@app.patch('/voyages/prix/<int:voyage_id>')
def patch_prix(voyage_id, infos: dict):
    if not "prix" in infos:
        raise HTTPException(status_code=404, detail="Le json doit contenir le prix!")
    if infos['prix']<0:
        raise HTTPException(status_code=404, detail="Un prix ne peut pas être négatif!")

    modify_from_arg(Voyage, voyage_id, "prix", infos['prix'])

    session = get_connection()
    stmt = select(Voyage).where(Voyage.voyage_id == voyage_id)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()

@app.patch('/voyages/voyage_fini/<int:voyage_id>')
def patch_voyage_fini(voyage_id, infos: dict):
    if not "voyage_fini" in infos:
        raise HTTPException(status_code=404, detail="Le json doit contenir l'état du voyage!")
    if not isinstance(infos['voyage_fini'], bool):
        raise HTTPException(status_code=404, detail="La valeur doit être un Boolean!")

    modify_from_arg(Voyage, voyage_id, "voyage_fini", infos['voyage_fini'])

    session = get_connection()
    stmt = select(Voyage).where(Voyage.voyage_id == voyage_id)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return result.to_dict()


#Partie PUT
@app.put('/utilisateurs/<string:email>')
def put_utilisateurs(email, infos: dict):
    changement_email=False
    for cle in infos:
        if cle=="email" or cle=="nom" or cle=="prenom" or cle=="age" or cle=="mdp":
            message=verification_utilisateur(cle,infos[cle])
            if message!="OK":
                raise HTTPException(status_code=404, detail=message)
            else:
                if changement_email==False:
                    modify_from_arg(Utilisateur, email, cle, infos[cle])
                else:
                    modify_from_arg(Utilisateur, infos["email"], cle, infos[cle])
                if cle=="email":
                    changement_email=True
    if 'email' in infos:
        result=select_from_arg("*", Utilisateur, "email", infos['email'])
    else:
        result=select_from_arg("*", Utilisateur, "email", email)
    for u in result:
        print(u.to_dict())
    return [u.to_dict() for u in result]

@app.put('/voyages/<int:voyage_id>')
def put_voyages(voyage_id, infos: dict):
    for cle in infos:
        if cle=="prix" or cle=="voyage_fini" or cle=="lieu":
            message=verification_voyage(cle,infos[cle])
            if message!="OK":
                raise HTTPException(status_code=404, detail=message)
            else:
                modify_from_arg(Voyage, voyage_id, cle, infos[cle])
    if "jour" in infos and "mois" in infos and "annee" in infos:
        message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
        if message!="OK":
            raise HTTPException(status_code=404, detail=message)
        else:
            modify_from_arg(Voyage, voyage_id, "date", date(infos['annee'], infos['mois'], infos['jour']))
    result=select_from_arg("*", Voyage, "voyage_id", voyage_id)
    for v in result:
        print(v.to_dict())
    return [v.to_dict() for v in result]


#Partie Delete
@app.delete('/utilisateurs/<string:email>')
def delete_utilisateur(email):
    message=verifier_email(email) #C'est a cause de cette fonction que verifier_existence_email n'est pas inclus dans verifier_email()
    if message!="OK":
        raise HTTPException(status_code=404, detail=message)
    verif=verifier_existence_email(email)
    if verif==False: #Donc que l'email n'existe pas
        return "L'email n'existe pas!"

    result=select_from_arg("*", Utilisateur, "email", email)
    if not result:
        raise HTTPException(status_code=404, detail="Cet email n'existe pas!")

    delete_from_arg(Utilisateur, email)
    result=select_from_arg("*", Utilisateur, "email", email)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="Cet utilisateur a bien été effacé!")
    else:
        raise HTTPException(status_code=404, detail="Il semble qu'il y ait eu un problème.")

@app.delete('/voyages/<int:voyage_id>')
def delete_voyage(voyage_id):
    verif=verifier_existence_id(Voyage, "voyage_id", voyage_id)
    if verif==False:
        raise HTTPException(status_code=404, detail="Le voyage n'existe pas!")

    delete_from_arg(Voyage, voyage_id)

    result=select_from_arg("*", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        raise HTTPException(status_code=404, detail="Ce voyage a bien été effacé!")
    else:
        raise HTTPException(status_code=404, detail="Il semble qu'il y ait eu un problème.")

@app.delete('/relations', methods=['DELETE'])
def delete_relations(infos: dict):
    if not ("utilisateur_id" in infos and "voyage_id" in infos):
        raise HTTPException(status_code=404, detail="Il faut donner 2 arguments : utilisateur_id et voyage_id!")
    else:
        session=get_connection()
        stmt = select(RelationUtilisateurVoyage).where(
            RelationUtilisateurVoyage.utilisateur_id == infos['utilisateur_id'],
            RelationUtilisateurVoyage.voyage_id == infos['voyage_id']
        )
        result = session.execute(stmt).scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail="Cette relation n'existe pas!")

        session.delete(result)
        session.commit()

        stmt = select(RelationUtilisateurVoyage).where(
            RelationUtilisateurVoyage.utilisateur_id == infos['utilisateur_id'],
            RelationUtilisateurVoyage.voyage_id == infos['voyage_id']
        )
        result = session.execute(stmt).scalars().first()
        session.close()
        if not result:
            return {"message":"La relation a bien été effacé!"}
        else:
            raise HTTPException(status_code=404, detail="Il semble qu'il y ait eu un problème.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

#Il y a un check a email (doit être un string, ne pas être vide et correspondre a x@y.z)
#Il y a un check a prenom (doit être un string et ne pas être vide)
#Il y a un check a nom (doit être un string et ne pas être vide)
#Il y a un check a age (age doit être supérieur ou égale a 0)
#Il y a un check a mdp (doit être un string et ne pas être vide)
#Il y a un check a prix (prix doit être supérieur ou égale a 0)
#Un a date (date doit être conforme (jour entre 0 et 31 ou 30 ou 29 ou 28 et mois entre 1 et 12)
#Un a voyage_fini (doit être un boolean)
#Un a lieu (doit être un string et ne pas être vide)
#Quand on fait un get l'email ou le voyage id doivent exister
#Quand on fait un POST, un Patch ou un Put sur les utilisateurs il faut que le nouvel email ne soit pas pré-existants

#Pas besoin de méthode Put ou Patch pour relation, ca ne sert a rien. Les id ne sont modifiables.
