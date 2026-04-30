from Verification import *
from Table_Classes import *
from Petites_Methodes import *
from datetime import date
from flask import Flask, jsonify, request

app=Flask(__name__)

@app.route('/')
def home():
    return ("Bienvenue dans l'API de gestion des utilisateurs! \n"
            "Voici les variables/colonnes utiles pour les différentes classes/tables:\n"
            "Utilisateurs: utilisateur_id, email (de la forme x@y.z), prenom, nom, age et mdp.\n"
            "Voyages: jour, mois et annee (seront combiné dans une seule variable/colonne nommé date, lieu, voyage_fini (True ou False) et prix\n"
            "Relations_Utilisateur_Voyage: utilisateur_id et voyage_id")

@app.route('/utilisateurs', methods=['POST'])
def post_utilisateur():
    infos=request.get_json()
    #Vérifier qu'infos contient bien toutes les infos

    if not ("email" in infos and "prenom" in infos and "nom" in infos and "age" in infos and "mdp" in infos):
        return jsonify({"message":"Le json doit contenir l'email, le prénom, le nom, l'âge et le mot de passe!"}),404
    message=verifier_email(infos['email'])
    if message!="OK":
        return jsonify({"message":message}),404
    verif=verifier_existence_email(infos['email'])
    if verif==True: #Donc que l'email existe
        return jsonify({"message":"L'email existe déja!"}),404

    message=verifier_str(infos['prenom'],"prenom")
    if message!="OK":
        return jsonify({"message":message}),404

    message=verifier_str(infos['nom'],"nom")
    if message!="OK":
        return jsonify({"message":message}),404

    if not isinstance(infos['age'], int):
        return jsonify({"message":"Un age doit être un Integer!"}),404
    if infos['age']<0:
        return jsonify({"message":"L'âge doit être supérieur ou égale a 0!"}),404

    message=verifier_str(infos['mdp'],"mdp")
    if message!="OK":
        return jsonify({"message":message}),404

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
    return jsonify(result.to_dict()),201
    #Le code 201 pour dire création réussie

@app.route('/voyages', methods=['POST'])
def post_voyage():
    infos=request.get_json()
    if not ("jour" in infos and "mois" in infos and "annee" in infos and "lieu" in infos and "prix" in infos):
        return jsonify({"message":"Le json doit contenir le jour, le mois, l'année, le lieu, l'état du voyage (fini ou non/True ou False) et le prix!"}),404

    message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
    if message!="OK":
        return jsonify({"message":message}),404

    message=verifier_str(infos['lieu'],"lieu")
    if message!="OK":
        return jsonify({"message":message}),404

    if not isinstance(infos['prix'], int) and not isinstance(infos['prix'], float) :
        return jsonify({"message":"Un prix doit être un Integer ou un Float!"}),404
    if infos['prix']<0:
        return jsonify({"message":"Un prix ne peut pas être négatif!"}),404

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
    return jsonify(result.to_dict()),201
    #Le code 201 pour dire création réussie

@app.route('/relations', methods=['POST'])
def post_relation():
    infos=request.get_json()
    if not("utilisateur_id" in infos and "voyage_id" in infos):
        return jsonify({"message":"Le json doit contenir l'id du participant et l'id du voyage!"}),404
    verif=verifier_existence_id(Utilisateur, "utilisateur_id", infos['utilisateur_id'])
    if verif==False: #Donc que l'email n'existe pas
        return jsonify({"message":"Cet utilisateur n'existe pas!"}),404
    verif=verifier_existence_id(Voyage, "voyage_id", infos['voyage_id'])
    if verif==False: #Donc que le voyage n'existe pas
        return jsonify({"message":"Ce voyage n'existe pas!"}),404
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
    return jsonify(result.to_dict()),201
    #Le code 201 pour dire création réussie

#Partie Get
@app.route('/utilisateurs', methods=['GET'])
#Méthode HTTP GET qui permet de retourner la liste des utilisateurs
def get_utilisateurs():
    #jsonify transforme result en json
    session = get_connection()
    stmt = select(Utilisateur)
    result = session.execute(stmt).scalars().all()
    for u in result:
        print(u.to_dict())
    session.close()
    return jsonify([u.to_dict() for u in result]), 200

@app.route('/utilisateurs/nom/<string:email>', methods=['GET'])
#On peut tester avec http://127.0.0.1:5000/utilisateurs/mdp/Test@test.com par exemple
def get_nom_by_email(email):
    result=select_from_arg("nom", Utilisateur, "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/utilisateurs/prenom/<string:email>', methods=['GET'])
def get_prenom_by_email(email):
    result=select_from_arg("prenom", Utilisateur, "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/utilisateurs/age/<string:email>', methods=['GET'])
def get_age_by_email(email):
    result=select_from_arg("age", Utilisateur, "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/utilisateurs/mdp/<string:email>', methods=['GET'])
def get_mdp_by_email(email):
    result=select_from_arg("mdp", Utilisateur, "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/utilisateurs/all/<string:email>', methods=['GET'])
def get_all_by_email(email):
    result=select_from_arg("*", Utilisateur, "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify([u.to_dict() for u in result]),200


@app.route('/voyages', methods=['GET'])
#Méthode HTTP GET qui permet de retourner la liste des utilisateurs
def get_voyages():
    session = get_connection()
    stmt = select(Voyage)
    result = session.execute(stmt).scalars().all()
    for u in result:
        print(u.to_dict())
    session.close()
    return jsonify([u.to_dict() for u in result]), 200

@app.route('/voyages/date/<int:voyage_id>', methods=['GET'])
def get_date_by_voyage_id(voyage_id):
    result=select_from_arg("date", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/voyages/lieu/<int:voyage_id>', methods=['GET'])
def get_lieu_by_voyage_id(voyage_id):
    result=select_from_arg("lieu", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/voyages/voyage_fini/<int:voyage_id>', methods=['GET'])
def get_voyage_fini_by_voyage_id(voyage_id):
    result=select_from_arg("voyage_fini", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/voyages/prix/<int:voyage_id>', methods=['GET'])
def get_prix_by_voyage_id(voyage_id):
    result=select_from_arg("prix", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/voyages/all/<int:voyage_id>', methods=['GET'])
def get_all_voyages_by_voyage_id(voyage_id):
    result=select_from_arg("*", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify([u.to_dict() for u in result]),200


@app.route('/relations', methods=['GET'])
def get_relations():
    session = get_connection()
    stmt = select(RelationUtilisateurVoyage)
    result = session.execute(stmt).scalars().all()
    for u in result:
        print(u.to_dict())
    session.close()
    return jsonify([u.to_dict() for u in result]), 200

@app.route('/relations/voyage_id/<int:utilisateur_id>', methods=['GET'])
#Vous donnez l'id de l'utilisateur ca sort les id de tous les voyages qu'il a fait
def get_voyage_id_by_email(utilisateur_id):
    result=select_from_arg("voyage_id", RelationUtilisateurVoyage, "utilisateur_id", utilisateur_id)
    if len(result)==0:
        return jsonify({"erreur":"La relation n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

@app.route('/relations/utilisateur_id/<int:voyage_id>', methods=['GET'])
def get_email_by_voyage_id(voyage_id):
    result=select_from_arg("utilisateur_id", RelationUtilisateurVoyage, "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"La relation n'existe pas !"}),404
    else :
        return jsonify([u for u in result]),200

#Les deux méthodes précedentes et les deux suivantes servent a la même chose mais je les ai quand même mis. On sait jamais.

@app.route('/relations/all/utilisateur_id/<int:utilisateur_id>', methods=['GET'])
def get_all_by_utilisateur_id(utilisateur_id):
    result=select_from_arg("*", RelationUtilisateurVoyage, "utilisateur_id", utilisateur_id)
    if len(result)==0:
        return jsonify({"erreur":"L'email n'est dans pas dans la table!"}),404
    else :
        return jsonify([u.to_dict() for u in result]),200

@app.route('/relations/all/voyage_id/<int:voyage_id>', methods=['GET'])
def get_all_relations_by_voyage_id(voyage_id):
    result=select_from_arg("*", RelationUtilisateurVoyage, "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"L'id n'est dans pas dans la table!"}),404
    else :
        return jsonify([u.to_dict() for u in result]),200

@app.route('/relations/one_line', methods=['GET'])
def get_one_line_relations():
    infos=request.get_json()
    if "utilisateur_id" in infos and "voyage_id" in infos:
        session = get_connection()
        stmt = select(RelationUtilisateurVoyage).where(
            RelationUtilisateurVoyage.utilisateur_id == infos["utilisateur_id"],
            RelationUtilisateurVoyage.voyage_id == infos["voyage_id"]
        )
        result = session.execute(stmt).scalars().first()
        session.close()
        if not result:
            return jsonify({"erreur":"Cette relation n'existe pas!"}),404
        else :
            return jsonify(result.to_dict()),200
    else:
        return jsonify({"erreur":"Il faut donner 2 arguments : utilisateur_id et voyage_id!"}),404

#Partie Patch
@app.route('/utilisateurs/email/<string:email>', methods=['PATCH'])
def patch_email(email):
    #Rajouter un garde fou, le nouvel email ne doit pas exister
    infos=request.get_json()
    if not "email" in infos:
        return jsonify({"message":"Le json doit contenir l'email!"}),404
    message=verifier_email(infos['email'])
    if message!="OK":
        return jsonify({"message":message}),404
    verif=verifier_existence_email(infos['email'])
    if verif==True: #Donc que l'email existe
        return jsonify({"message":"L'email existe déja!"}),404

    modify_from_arg(Utilisateur, email, "email", infos['email'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == infos['email'])
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200

@app.route('/utilisateurs/prenom/<string:email>', methods=['PATCH'])
def patch_prenom(email):
    infos=request.get_json()
    if not "prenom" in infos:
        return jsonify({"message":"Le json doit contenir le prénom!"}),404
    message=verifier_str(infos['prenom'],"prénom")
    if message!="OK":
        return jsonify({"message":message}),404

    modify_from_arg(Utilisateur, email, "prenom", infos['prenom'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200

@app.route('/utilisateurs/nom/<string:email>', methods=['PATCH'])
def patch_nom(email):
    infos=request.get_json()
    if not "nom" in infos:
        return jsonify({"message":"Le json doit contenir le nom!"}),404
    message=verifier_str(infos['nom'],"nom")
    if message!="OK":
        return jsonify({"message":message}),404

    modify_from_arg(Utilisateur, email, "nom", infos['nom'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200

@app.route('/utilisateurs/age/<string:email>', methods=['PATCH'])
def patch_age(email):
    infos=request.get_json()
    if not "age" in infos:
        return jsonify({"message":"Le json doit contenir l'âge!"}),404
    if infos['age']<0:
        return jsonify({"message":"L'âge doit être supérieur ou égale a 0!"}),404

    modify_from_arg(Utilisateur, email, "age", infos['age'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200

@app.route('/utilisateurs/mdp/<string:email>', methods=['PATCH'])
def patch_mdp(email):
    infos=request.get_json()
    if not "mdp" in infos:
        return jsonify({"message":"Le json doit contenir le mot de passe!"}),404
    message=verifier_str(infos['mdp'],"mdp")
    if message!="OK":
        return jsonify({"message":message}),404

    modify_from_arg(Utilisateur, email, "mdp", infos['mdp'])

    session = get_connection()
    stmt = select(Utilisateur).where(Utilisateur.email == email)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200


@app.route('/voyages/date/<int:voyage_id>', methods=['PATCH'])
def patch_date(voyage_id):
    infos=request.get_json()
    if not ("jour" in infos and "mois" in infos and "annee" in infos):
        return jsonify({"message":"Le json doit contenir le jour, le mois et l'année!"}),404
    message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
    if message!="OK":
        return jsonify({"message":message}),404

    modify_from_arg(Voyage, voyage_id, "date", date(infos['annee'], infos['mois'], infos['jour']))

    session = get_connection()
    stmt = select(Voyage).where(Voyage.voyage_id == voyage_id)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200

@app.route('/voyages/lieu/<int:voyage_id>', methods=['PATCH'])
def patch_lieu(voyage_id):
    infos=request.get_json()
    if not "lieu" in infos:
        return jsonify({"message":"Le json doit contenir le lieu!"}),404
    message=verifier_str(infos['lieu'],"lieu")
    if message!="OK":
        return jsonify({"message":message}),404

    modify_from_arg(Voyage, voyage_id, "lieu", infos['lieu'])

    session = get_connection()
    stmt = select(Voyage).where(Voyage.voyage_id == voyage_id)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200

@app.route('/voyages/prix/<int:voyage_id>', methods=['PATCH'])
def patch_prix(voyage_id):
    infos=request.get_json()
    if not "prix" in infos:
        return jsonify({"message":"Le json doit contenir le prix!"}),404
    if infos['prix']<0:
        return jsonify({"message":"Un prix ne peut pas être négatif!"}),404

    modify_from_arg(Voyage, voyage_id, "prix", infos['prix'])

    session = get_connection()
    stmt = select(Voyage).where(Voyage.voyage_id == voyage_id)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200

@app.route('/voyages/voyage_fini/<int:voyage_id>', methods=['PATCH'])
def patch_voyage_fini(voyage_id):
    infos=request.get_json()
    if not "voyage_fini" in infos:
        return jsonify({"message":"Le json doit contenir l'état du voyage!"}),404
    if not isinstance(infos['voyage_fini'], bool):
        return jsonify({"message":"La valeur doit être un Boolean!"}),404

    modify_from_arg(Voyage, voyage_id, "voyage_fini", infos['voyage_fini'])

    session = get_connection()
    stmt = select(Voyage).where(Voyage.voyage_id == voyage_id)
    result = session.execute(stmt).scalars().first()
    print(result.to_dict())
    session.close()
    return jsonify(result.to_dict()), 200


#Partie PUT
@app.route('/utilisateurs/<string:email>', methods=['PUT'])
def put_utilisateurs(email):
    infos=request.get_json()
    changement_email=False
    for cle in infos:
        if cle=="email" or cle=="nom" or cle=="prenom" or cle=="age" or cle=="mdp":
            message=verification_utilisateur(cle,infos[cle])
            if message!="OK":
                return jsonify({"message":message}),404
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
    return jsonify([u.to_dict() for u in result]), 200

@app.route('/voyages/<int:voyage_id>', methods=['PUT'])
def put_voyages(voyage_id):
    infos=request.get_json()
    for cle in infos:
        if cle=="prix" or cle=="voyage_fini" or cle=="lieu":
            message=verification_voyage(cle,infos[cle])
            if message!="OK":
                return jsonify({"message":message}),404
            else:
                modify_from_arg(Voyage, voyage_id, cle, infos[cle])
    if "jour" in infos and "mois" in infos and "annee" in infos:
        message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
        if message!="OK":
            return jsonify({"message":message}),404
        else:
            modify_from_arg(Voyage, voyage_id, "date", date(infos['annee'], infos['mois'], infos['jour']))
    result=select_from_arg("*", Voyage, "voyage_id", voyage_id)
    for v in result:
        print(v.to_dict())
    return jsonify([v.to_dict() for v in result]), 200


#Partie Delete

@app.route('/utilisateurs/<string:email>', methods=['DELETE'])
def delete_utilisateur(email):
    message=verifier_email(email) #C'est a cause de cette fonction que verifier_existence_email n'est pas inclus dans verifier_email()
    if message!="OK":
        return jsonify({"message":message}),404
    verif=verifier_existence_email(email)
    if verif==False: #Donc que l'email n'existe pas
        return "L'email n'existe pas!"

    result=select_from_arg("*", Utilisateur, "email", email)
    if not result:
        return jsonify({"message":"Cet email n'existe pas!"}), 404

    delete_from_arg(Utilisateur, email)
    result=select_from_arg("*", Utilisateur, "email", email)
    if len(result)==0:
        return jsonify({"message":"Cet utilisateur a bien été effacé!"}), 200
    else:
        return jsonify({"message":"Il semble qu'il y ait eu un problème."}), 404

@app.route('/voyages/<int:voyage_id>', methods=['DELETE'])
def delete_voyage(voyage_id):
    verif=verifier_existence_id(Voyage, "voyage_id", voyage_id)
    if verif==False:
        return jsonify({"message":"Le voyage n'existe pas!"}),404

    delete_from_arg(Voyage, voyage_id)
    result=select_from_arg("*", Voyage, "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"message":"Ce voyage a bien été effacé!"}), 200
    else:
        return jsonify({"message":"Il semble qu'il y ait eu un problème."}), 404

@app.route('/relations', methods=['DELETE'])
def delete_relations():
    infos=request.get_json()
    if not ("utilisateur_id" in infos and "voyage_id" in infos):
        return jsonify({"erreur":"Il faut donner 2 arguments : utilisateur_id et voyage_id!"}),404
    else:
        session=get_connection()
        stmt = select(RelationUtilisateurVoyage).where(
            RelationUtilisateurVoyage.utilisateur_id == infos['utilisateur_id'],
            RelationUtilisateurVoyage.voyage_id == infos['voyage_id']
        )
        result = session.execute(stmt).scalars().first()
        if not result:
            return jsonify({"message":"Cette relation n'existe pas!"}),404

        session.delete(result)
        session.commit()
        session.close()

        stmt = select(RelationUtilisateurVoyage).where(
            RelationUtilisateurVoyage.utilisateur_id == infos['utilisateur_id'],
            RelationUtilisateurVoyage.voyage_id == infos['voyage_id']
        )
        result = session.execute(stmt).scalars().first()
        if not result:
            return jsonify({"message":"La relation a bien été effacé!"}), 200
        else:
            return jsonify({"message":"Il semble qu'il y ait eu un problème."}), 404

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
