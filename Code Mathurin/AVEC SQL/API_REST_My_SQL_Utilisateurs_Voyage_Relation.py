#N'a pas été testé pour transformer plus vite en version PostgreSql
#Il y a des erreurs notamment au niveau des if "email" in infos et autres. PAr exemple pour ces derniers il faut mettre not devant
from flask import Flask, jsonify, request
from db_MySQL import get_connection
from datetime import date
import calendar
import re
app=Flask(__name__)

def select_from_arg(champ_retour, table, champ,valeur):
    conn=get_connection()
    cursor = conn.cursor()
    query=f"SELECT {champ_retour} FROM {table} WHERE {champ} = %s"
    print(query)
    cursor.execute(query, valeur)
    result=cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()
    return result

def modify_from_arg(table, champ_a_modifier, nouvelle_valeur, champ_reconnaissance, valeur_reconnaissance):
    conn=get_connection()
    cursor = conn.cursor()
    query=f"UPDATE {table} SET {champ_a_modifier} = %s WHERE {champ_reconnaissance} = %s"
    cursor.execute(query, (nouvelle_valeur, valeur_reconnaissance))
    conn.commit()
    cursor.close()
    conn.close()

def delete_from_arg(table, champ_reconnaissance, valeur_reconnaissance):
    conn=get_connection()
    cursor = conn.cursor()
    query=f"DELETE FROM {table} WHERE {champ_reconnaissance} = %s"
    cursor.execute(query, valeur_reconnaissance)
    conn.commit()
    cursor.close()
    conn.close()

def verifier_str(info, nom):
    if not isinstance(info, str):
        return f"Un {nom} doit être un String!"
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
    conn=get_connection()
    cursor = conn.cursor()
    query="SELECT * FROM utilisateurs WHERE email=%s"
    cursor.execute(query,email)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return False
    else:
        return True

def verifier_existence_id(table, variable, id):
    conn=get_connection()
    cursor = conn.cursor()
    query=f"SELECT * FROM {table} WHERE {variable}=%s"
    cursor.execute(query,id)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return False
    else:
        return True

def verifier_date(jour, mois, annee):
    if mois not in range(1,12):
        return "Mois dois être entre 1 et 12!"
    else:
        if mois in range(1,7,2) or mois in range(8,12,2):
            if jour not in range(1,31):
                return "Jour dois être entre 1 et 31!"
        else:
            if mois in range(4,6,2) or mois in range(9,11,2):
                if jour not in range(1,30):
                    return "Jour dois être entre 1 et 30!"
            else: #donc que mois=2
                if calendar.isleap(annee): #Si année bissextile
                    if jour not in range(1,29):
                        return "Jour dois être entre 1 et 29!"
                else: #Si année pas bissextile
                    if jour not in range(1,28):
                        return "Jour dois être entre 1 et 28!"
    return "OK"

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

@app.route('/')
def home():
    return ("Bienvenue dans l'API de gestion des utilisateurs! \n"
            "Voici les variables/colonnes utiles pour les différentes classes/tables:\n"
            "Utilisateurs: email (de la forme x@y.z), prenom, nom, age et mdp.\n"
            "Voyages: jour, mois et annee (seront combiné dans une seule variable/colonne nommé date, lieu, voyage_fini (True ou False) et prix\n"
            "Relations_Utilisateur_Voyage: email et voyage_id")

#Partie POST

@app.route('/utilisateurs', methods=['POST'])
def post_utilisateur():
    infos=request.get_json()
    #Vérifier qu'infos contient bien toutes les infos
    if "email" in infos and "prenom" in infos and "nom" in infos and "age" in infos and "mdp" in infos:
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
    if infos['age']<0:
        return jsonify({"message":"L'âge doit être supérieur ou égale a 0!"}),404
    message=verifier_str(infos['mdp'],"mdp")
    if message!="OK":
        return jsonify({"message":message}),404
    conn=get_connection()
    cursor = conn.cursor()
    query="INSERT INTO utilisateurs (email, prenom, nom, age, mdp) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query, (infos['email'], infos['prenom'], infos['nom'], infos['age'], infos['mdp']))
    conn.commit()
    query="SELECT * FROM utilisateurs WHERE email=%s"
    cursor.execute(query,infos['email'])
    result=cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()
    return jsonify(result),201
    #Le code 201 pour dire création réussie

@app.route('/voyages', methods=['POST'])
def post_voyage():
    infos=request.get_json()
    if "jour" in infos and "mois" in infos and "annee" in infos and "lieu" in infos and "voyage_fini" in infos and "prix" in infos:
        return jsonify({"message":"Le json doit contenir le jour, le mois, l'année, le lieu, l'état du voyage (fini ou non/True ou False) et le prix!"}),404
    message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
    if message!="OK":
        return jsonify({"message":message}),404
    message=verifier_str(infos['lieu'],"lieu")
    if message!="OK":
        return jsonify({"message":message}),404
    if not isinstance(infos['voyage_fini'], bool):
        return jsonify({"message":"La valeur doit être un Boolean!"}),404
    if infos['prix']<0:
        return jsonify({"message":"Un prix ne peut pas être négatif!"}),404
    conn=get_connection()
    cursor = conn.cursor()
    query="INSERT INTO voyages (date, lieu, voyage_fini, prix) VALUES (%s,%s,%s,%s)"
    date_inscription = date(infos['annee'], infos['mois'], infos['jour'])
    cursor.execute(query, (date_inscription, infos['lieu'], False, infos['prix']))
    conn.commit()
    query="SELECT MAX(voyage_id) FROM voyages"
    cursor.execute(query)
    v_id=cursor.fetchall()
    query="SELECT * FROM voyages WHERE voyage_id=%s"
    cursor.execute(query, v_id)
    result=cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()
    return jsonify(result),201
    #Le code 201 pour dire création réussie

@app.route('/relations', methods=['POST'])
def post_relation():
    infos=request.get_json()
    if "utilisateur" in infos and "voyage_id" in infos:
        return jsonify({"message":"Le json doit contenir l'email du participant et l'id du voyage!"}),404
    verif=verifier_existence_id("utilisateurs", "utilisateur_id", infos['utilisateur_id'])
    if verif==False: #Donc que l'email n'existe pas
        return jsonify({"message":"Cet utilisateur n'existe pas!"}),404
    verif=verifier_existence_id("voyages", "voyage_id", infos['voyage_id'])
    if verif==False: #Donc que le voyage n'existe pas
        return jsonify({"message":"Ce voyage n'existe pas!"}),404
    #Pas besoin de plus de vérification. Comme les emails et les ids doivent être préexistants ca veut dire qu'ils ont passé les checks.
    conn=get_connection()
    cursor = conn.cursor()
    query="INSERT INTO relation_utilisateur_voyage (utilisateur_id, voyage_id) VALUES (%s,%s)"
    cursor.execute(query, (infos['utilisateur_id'], infos['voyage_id']))
    conn.commit()
    query="SELECT * FROM relation_utilisateur_voyage WHERE utilisateur_id=%s AND voyage_id=%s"
    cursor.execute(query,(infos['utilisateur_id'], infos['voyage_id']))
    result=cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()
    return jsonify(result),201
    #Le code 201 pour dire création réussie

#Partie Get
@app.route('/utilisateurs', methods=['GET'])
#Méthode HTTP GET qui permet de retourner la liste des utilisateurs
def get_utilisateurs():
    #jsonify transforme result en json
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * from utilisateurs")
    result=cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()
    return jsonify(result), 200

@app.route('/utilisateurs/nom/<string:email>', methods=['GET'])
#On peut tester avec http://127.0.0.1:5000/utilisateurs/mdp/Test@test.com par exemple
def get_nom_by_email(email):
    result=select_from_arg("nom", "utilisateurs", "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/utilisateurs/prenom/<string:email>', methods=['GET'])
def get_prenom_by_email(email):
    result=select_from_arg("prenom", "utilisateurs", "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/utilisateurs/age/<string:email>', methods=['GET'])
def get_age_by_email(email):
    result=select_from_arg("age", "utilisateurs", "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/utilisateurs/mdp/<string:email>', methods=['GET'])
def get_mdp_by_email(email):
    result=select_from_arg("mdp", "utilisateurs", "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/utilisateurs/all/<string:email>', methods=['GET'])
def get_all_by_email(email):
    result=select_from_arg("*", "utilisateurs", "email", email)
    if len(result)==0:
        return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404
    else :
        return jsonify(result),200


@app.route('/voyages', methods=['GET'])
#Méthode HTTP GET qui permet de retourner la liste des utilisateurs
def get_voyages():
    #jsonify transforme la liste students en json
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * from voyages")
    result=cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()
    return jsonify(result), 200

@app.route('/voyages/date/<int:voyage_id>', methods=['GET'])
def get_date_by_voyage_id(voyage_id):
    result=select_from_arg("date", "voyages", "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/voyages/lieu/<int:voyage_id>', methods=['GET'])
def get_lieu_by_voyage_id(voyage_id):
    result=select_from_arg("lieu", "voyages", "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/voyages/voyage_fini/<int:voyage_id>', methods=['GET'])
def get_voyage_fini_by_voyage_id(voyage_id):
    result=select_from_arg("voyage_fini", "voyages", "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/voyages/prix/<int:voyage_id>', methods=['GET'])
def get_prix_by_voyage_id(voyage_id):
    result=select_from_arg("prix", "voyages", "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/voyages/all/<int:voyage_id>', methods=['GET'])
def get_all_voyages_by_voyage_id(voyage_id):
    result=select_from_arg("*", "voyages", "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"Le voyage n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/relations', methods=['GET'])
def get_relations():
    conn=get_connection()
    cursor = conn.cursor()
    query="SELECT * FROM relation_utilisateur_voyage"
    cursor.execute(query)
    result=cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()
    return jsonify(result),200

@app.route('/relations/voyage_id/<int:utilisateur_id>', methods=['GET'])
#Vous donnez l'id de l'utilisateur ca sort les id de tous les voyages qu'il a fait
def get_voyage_id_by_email(utilisateur_id):
    result=select_from_arg("voyage_id", "relation_utilisateur_voyage", "utilisateur_id", utilisateur_id)
    if len(result)==0:
        return jsonify({"erreur":"La relation n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/relations/int:utilisateur_id/<int:voyage_id>', methods=['GET'])
def get_email_by_voyage_id(voyage_id):
    result=select_from_arg("int:utilisateur_id", "relation_utilisateur_voyage", "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"La relation n'existe pas !"}),404
    else :
        return jsonify(result),200

@app.route('/relations/all/utilisateur_id/<int:utilisateur_id>', methods=['GET'])
def get_all_by_utilisateur_id(utilisateur_id):
    result=select_from_arg("*", "relation_utilisateur_voyage", "utilisateur_id", utilisateur_id)
    if len(result)==0:
        return jsonify({"erreur":"L'email n'est dans pas dans la table!"}),404
    else :
        return jsonify(result),200

@app.route('/relations/all/voyage_id/<int:voyage_id>', methods=['GET'])
def get_all_relations_by_voyage_id(voyage_id):
    result=select_from_arg("*", "relation_utilisateur_voyage", "voyage_id", voyage_id)
    if len(result)==0:
        return jsonify({"erreur":"L'id n'est dans pas dans la table!"}),404
    else :
        return jsonify(result),200

@app.route('/relations/one_line', methods=['GET'])
def get_one_line_relations():
    infos=request.get_json()
    if "utilisateur_id" in infos and "voyage_id" in infos:
        conn=get_connection()
        cursor = conn.cursor()
        query="SELECT * FROM relation_utilisateur_voyage WHERE utilisateur_id=%s AND voyage_id=%s"
        cursor.execute(query,(infos['utilisateur_id'],infos['voyage_id']))
        result=cursor.fetchall()
        print(result)
        cursor.close()
        conn.close()
        if len(result)==0:
            return jsonify({"erreur":"Cette relation n'existe pas!"}),404
        else :
            return jsonify(result),200
    else:
        return jsonify({"erreur":"Il faut donner 2 arguments : utilisateur_id et voyage_id!"}),404

#Partie Patch
@app.route('/utilisateurs/email/<string:email>', methods=['PATCH'])
def patch_email(email):
    #Rajouter un garde fou, le nouvel email ne doit pas exister
    infos=request.get_json()
    if "email" in infos:
        return jsonify({"message":"Le json doit contenir l'email!"}),404
    message=verifier_email(infos['email'])
    if message!="OK":
        return jsonify({"message":message}),404
    verif=verifier_existence_email(infos['email'])
    if verif==True: #Donc que l'email existe
        return jsonify({"message":"L'email existe déja!"}),404
    modify_from_arg("utilisateurs", "email", infos['email'], "email", email)
    result=select_from_arg("*", "utilisateurs", "email", infos['email'])
    print(result)
    return jsonify(result)

@app.route('/utilisateurs/prenom/<string:email>', methods=['PATCH'])
def patch_prenom(email):
    infos=request.get_json()
    if "prenom" in infos:
        return jsonify({"message":"Le json doit contenir le prénom!"}),404
    message=verifier_str(infos['prenom'],"prénom")
    if message!="OK":
        return jsonify({"message":message}),404
    modify_from_arg("utilisateurs", "prenom", infos['prenom'], "email", email)
    result=select_from_arg("*", "utilisateurs", "email", email)
    print(result)
    return jsonify(result)

@app.route('/utilisateurs/nom/<string:email>', methods=['PATCH'])
def patch_nom(email):
    infos=request.get_json()
    if "nom" in infos:
        return jsonify({"message":"Le json doit contenir le nom!"}),404
    message=verifier_str(infos['nom'],"nom")
    if message!="OK":
        return jsonify({"message":message}),404
    modify_from_arg("utilisateurs", "nom", infos['nom'], "email", email)
    result=select_from_arg("*", "utilisateurs", "email", email)
    print(result)
    return jsonify(result)

@app.route('/utilisateurs/age/<string:email>', methods=['PATCH'])
def patch_age(email):
    infos=request.get_json()
    if "age" in infos:
        return jsonify({"message":"Le json doit contenir l'âge!"}),404
    if infos['age']<0:
        return jsonify({"message":"L'âge doit être supérieur ou égale a 0!"}),404
    modify_from_arg("utilisateurs", "age", infos['age'], "email", email)
    result=select_from_arg("*", "utilisateurs", "email", email)
    print(result)
    return jsonify(result)

@app.route('/utilisateurs/mdp/<string:email>', methods=['PATCH'])
def patch_mdp(email):
    infos=request.get_json()
    if "mdp" in infos:
        return jsonify({"message":"Le json doit contenir le mot de passe!"}),404
    message=verifier_str(infos['mdp'],"mdp")
    if message!="OK":
        return jsonify({"message":message}),404
    modify_from_arg("utilisateurs", "mdp", infos['mdp'], "email", email)
    result=select_from_arg("*", "utilisateurs", "email", email)
    print(result)
    return jsonify(result)


@app.route('/voyages/date/<int:voyage_id>', methods=['PATCH'])
def patch_date(voyage_id):
    infos=request.get_json()
    if "jour" in infos and "mois" in infos and "annee" in infos:
        return jsonify({"message":"Le json doit contenir le jour, le mois et l'année!"}),404
    message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
    if message!="OK":
        return jsonify({"message":message}),404
    modify_from_arg("voyages", "date", date(infos['annee'], infos['mois'], infos['jour']), "voyage_id", voyage_id)
    result=select_from_arg("*", "voyages", "voyage_id", voyage_id)
    print(result)
    return jsonify(result)

@app.route('/voyages/lieu/<int:voyage_id>', methods=['PATCH'])
def patch_lieu(voyage_id):
    infos=request.get_json()
    if "lieu" in infos:
        return jsonify({"message":"Le json doit contenir le lieu!"}),404
    message=verifier_str(infos['lieu'],"lieu")
    if message!="OK":
        return jsonify({"message":message}),404
    modify_from_arg("voyages", "lieu", infos['lieu'], "voyage_id", voyage_id)
    result=select_from_arg("*", "voyages", "voyage_id", voyage_id)
    print(result)
    return jsonify(result)

@app.route('/voyages/prix/<int:voyage_id>', methods=['PATCH'])
def patch_prix(voyage_id):
    infos=request.get_json()
    if "prix" in infos:
        return jsonify({"message":"Le json doit contenir le prix!"}),404
    if infos['prix']<0:
        return jsonify({"message":"Un prix ne peut pas être négatif!"}),404
    modify_from_arg("voyages", "prix", infos['prix'], "voyage_id", voyage_id)
    result=select_from_arg("*", "voyages", "voyage_id", voyage_id)
    print(result)
    return jsonify(result)

@app.route('/voyages/voyage_fini/<int:voyage_id>', methods=['PATCH'])
def patch_voyage_fini(voyage_id):
    infos=request.get_json()
    if "voyage_fini" in infos:
        return jsonify({"message":"Le json doit contenir l'état du voyage!"}),404
    if not isinstance(infos['voyage_fini'], bool):
        return jsonify({"message":"La valeur doit être un Boolean!"}),404
    modify_from_arg("voyages", "voyage_fini", infos['voyage_fini'], "voyage_id", voyage_id)
    result=select_from_arg("*", "voyages", "voyage_id", voyage_id)
    print(result)
    return jsonify(result)

#Partie PUT
@app.route('/utilisateurs/<string:email>', methods=['PUT'])
def put_utilisateurs(email):
    infos=request.get_json()
    for cle in infos:
        if cle=="email" or cle=="nom" or cle=="prenom" or cle=="age" or cle=="mdp":
            message=verification_utilisateur(cle,infos['cle'])
            if message!="OK":
                return jsonify({"message":message}),404
            else:
                modify_from_arg("utilisateurs", cle, infos[cle], "email", email)
    if 'email' in infos:
        result=select_from_arg("*", "utilisateurs", "email", infos['email'])
    else:
        result=select_from_arg("*", "utilisateurs", "email", email)
    print(result)
    return jsonify(result)


@app.route('/voyages/<int:voyage_id>', methods=['PUT'])
def put_voyages(voyage_id):
    infos=request.get_json()
    for cle in infos:
        if cle=="prix" or cle=="voyage_fini" or cle=="lieu":
            message=verification_voyage(cle,infos[cle])
            if message!="OK":
                return jsonify({"message":message}),404
            else:
                modify_from_arg("voyages", cle, infos[cle], "voyage_id", voyage_id)
    if "jour" in infos and "mois" in infos and "annee" in infos:
        message=verifier_date(infos['jour'], infos['mois'], infos['annee'])
        if message!="OK":
            return jsonify({"message":message}),404
        else:
            modify_from_arg("voyages", "date", date(infos['annee'], infos['mois'], infos['jour']), "voyage_id", voyage_id)
    result=select_from_arg("*", "voyages", "voyage_id", voyage_id)
    print(result)
    return jsonify(result)

#Partie Delete
#Faire pareil pour la table relation utilisateur_voyage

@app.route('/utilisateurs/<string:email>', methods=['DELETE'])
def delete_utilisateur(email):
    message=verifier_email(email) #C'est a cause de cette fonction que verifier_existence_email n'est pas inclus dans verifier_email()
    if message!="OK":
        return jsonify({"message":message}),404
    verif=verifier_existence_email(email)
    if verif==False: #Donc que l'email n'existe pas
        return "L'email n'existe pas!"
    conn=get_connection()
    cursor = conn.cursor()
    query="SELECT * FROM utilisateurs WHERE email=%s"
    cursor.execute(query,email)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return "Cet email n'existe pas!"
    else:
        delete_from_arg("utilisateurs", "email", email)
        return get_utilisateurs()

@app.route('/voyages/<int:voyage_id>', methods=['DELETE'])
def delete_voyage(voyage_id):
    conn=get_connection()
    cursor = conn.cursor()
    query="SELECT * FROM voyages WHERE voyage_id=%s"
    cursor.execute(query,voyage_id)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return "Ce voyage n'existe pas!"
    delete_from_arg("voyages", "voyage_id", voyage_id)
    return get_voyages()

@app.route('/relations', methods=['DELETE'])
def delete_relations():
    infos=request.get_json()
    if not ("utilisateur_id" in infos and "voyage_id" in infos):
        return jsonify({"erreur":"Il faut donner 2 arguments : utilisateur_id et voyage_id!"}),404
    else:
        verif=verifier_existence_id("relation_utilisateur_voyage", "utilisateur_id", infos['utilisateur_id'])
        if verif==False: #Donc que le voyage n'existe pas
            return jsonify({"message":"Cette relation n'existe pas!"}),404
        verif=verifier_existence_id("relation_utilisateur_voyage", "voyage_id", infos['voyage_id'])
        if verif==False: #Donc que le voyage n'existe pas
            return jsonify({"message":"Cette relation n'existe pas!"}),404
        conn=get_connection()
        cursor = conn.cursor()
        query=f"DELETE FROM relation_utilisateur_voyage WHERE utilisateur_id=%s AND voyage_id=%s"
        cursor.execute(query,(infos['utilisateur_id'],infos['voyage_id']))
        cursor.close()
        conn.close()
        return get_relations()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

#Rajouter erreur 404
#if not utilisateur:
#return jsonify({"message":"Utilisateur non trouvé !"}),404

#Tester les différents checks
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
