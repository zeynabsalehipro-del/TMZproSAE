from flask import Flask, jsonify, request
from Utilisateur import Utilisateur
app=Flask(__name__)

u = Utilisateur("Test@test.com", "Te", "St", 1, "Test")
utilisateurs=[u]

def listifier(utilisateurs):
    users=[]
    for utilisateur in utilisateurs:
        users.append(utilisateur.liste_attributs())
    return users

@app.route('/')
def home():
    return "Bienvenue dans l'API de gestion des utilisateurs!"

@app.route('/utilisateurs', methods=['GET'])
#Méthode HTTP GET qui permet de retourner la liste des utilisateurs
def get_utilisateur():
    "jsonify transforme la liste students en json"
    return jsonify(listifier(utilisateurs))

@app.route('/utilisateurs', methods=['POST'])
def add_utilisateur():
    infos=request.get_json()
    #Mettre des vérifications sur les données. Age!=String ou email contient @
    new_utilisateur=Utilisateur(infos['email'], infos['nom'], infos['prenom'], infos['age'], infos['mdp'])
    #Pour récupérer les données envoyé par le client
    utilisateurs.append(new_utilisateur)
    print("Utilisateurs:",utilisateurs)
    return jsonify(listifier(utilisateurs)),201
    #Le code 201 pour dire création réussie

@app.route('/utilisateurs/nom/<string:email>', methods=['GET'])
#On peut tester avec http://127.0.0.1:5000/utilisateurs/mdp/Test@test.com par exemple
def get_nom_by_email(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if utilisateur:
        return jsonify(utilisateur.get_nom())
    return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404

@app.route('/utilisateurs/prenom/<string:email>', methods=['GET'])
def get_prenom_by_email(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if utilisateur:
        return jsonify(utilisateur.get_prenom())
    return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404

@app.route('/utilisateurs/age/<string:email>', methods=['GET'])
def get_age_by_email(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if utilisateur:
        return jsonify(utilisateur.get_age())
    return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404

@app.route('/utilisateurs/mdp/<string:email>', methods=['GET'])
def get_mdp_by_email(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if utilisateur:
        return jsonify(utilisateur.get_mdp())
    return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404

@app.route('/utilisateurs/voyage_en_cours/<string:email>', methods=['GET'])
def get_voyages_en_cours_by_email(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if utilisateur:
        return jsonify(utilisateur.get_voyages_en_cours())
    return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404

@app.route('/utilisateurs/voyage_passes/<string:email>', methods=['GET'])
def get_voyages_passes_by_email(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if utilisateur:
        return jsonify(utilisateur.get_voyages_passes())
    return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404

@app.route('/utilisateurs/all/<string:email>', methods=['GET'])
def get_all_by_email(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if utilisateur:
        return jsonify(utilisateur.liste_attributs())
    return jsonify({"erreur":"l'utilisateur n'existe pas !"}),404

#Mettre a jour un étudiant PUT
#Juste pour tester
@app.route('/utilisateurs/email/<string:email>', methods=['PATCH'])
def update_email(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.set_email(data["email"]) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

#Mettre a jour un étudiant PUT
@app.route('/utilisateurs/nom/<string:email>', methods=['PATCH'])
def update_nom(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.set_nom(data["nom"]) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

#Mettre a jour un étudiant PUT
@app.route('/utilisateurs/prenom/<string:email>', methods=['PATCH'])
def update_prenom(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.set_prenom(data["prenom"]) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

#Mettre a jour un étudiant PUT
@app.route('/utilisateurs/age/<string:email>', methods=['PATCH'])
def update_age(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.set_age(data["age"]) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

#Mettre a jour un étudiant PUT
@app.route('/utilisateurs/mdp/<string:email>', methods=['PATCH'])
def update_mdp(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.set_mdp(data["mdp"]) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

#Mettre a jour un étudiant PUT
@app.route('/utilisateurs/all/<string:email>', methods=['PUT'])
def update_all(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.set_all(data) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

@app.route('/utilisateurs/voyage/<string:email>', methods=['PATCH'])
def ajoute_voyage(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.ajoute_voyage(data["v_id"]) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

@app.route('/utilisateurs/voyage_fini/<string:email>', methods=['PATCH'])
def voyage_fini(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.voyage_fini(data["v_id"]) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

@app.route('/utilisateurs/voyage/<string:email>', methods=['DELETE'])
def voyage_annule(email):
    utilisateur=next((u for u in utilisateurs if u.get_email()==email),None)
    if not utilisateur:
        return jsonify({"message":"Utilisateur non trouvé !"}),404
    data=request.get_json()
    print(data)
    utilisateur.voyage_annule(data["v_id"]) # Mise a jour des données
    return jsonify(utilisateur.liste_attributs())

if __name__=='__main__':
    app.run(debug=True)
