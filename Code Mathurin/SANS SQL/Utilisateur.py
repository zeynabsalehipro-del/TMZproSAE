class Utilisateur:
    def __init__(self, email, nom, prenom, age, mdp):
        if email is None or nom is None or prenom is None or age is None or mdp is None:
            print("Infos incomplètes.")
            return
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.mdp = mdp
        self.voyages_en_cours=[] #liste des voyages en cours ou futurs
        self.voyages_passes=[] #Liste des voyages passés
        print("Infos:",self.email, self.nom, self.prenom, self.age, self.mdp)

    def get_email(self):
        return self.email
    def get_nom(self):
        return self.nom
    def get_prenom(self):
        return self.prenom
    def get_age(self):
        return self.age
    def get_mdp(self):
        return self.mdp
    def get_voyages_en_cours(self):
        return self.voyages_en_cours
    def get_voyages_passes(self):
        return self.voyages_passes

    def set_email(self, email):
        self.email = email
    def set_nom(self, nom):
        self.nom = nom
    def set_prenom(self, prenom):
        self.prenom = prenom
    def set_age(self, age):
        self.age = age
    def set_mdp(self, mdp):
        self.mdp = mdp
    def set_all(self,data):
        if "email" in data:
            self.set_email(data["email"])
        if "nom" in data:
            self.set_nom(data["nom"])
        if "prenom" in data:
            self.set_prenom(data["prenom"])
        if "age" in data:
            self.set_age(data["age"])
        if "mdp" in data:
            self.set_mdp(data["mdp"])
    def ajoute_voyage(self,v_id):
        self.voyages_en_cours.append(v_id)
    def voyage_annule(self,v_id):
        self.voyages_en_cours.remove(v_id)
    def voyage_fini(self,v_id):
        self.voyages_en_cours.remove(v_id)
        self.voyages_passes.append(v_id)
    def liste_attributs(self):
        liste={};
        liste["email"]=self.get_email()
        liste["name"]=self.get_nom()
        liste["prenom"]=self.get_prenom()
        liste["age"]=self.get_age()
        liste["mdp"]=self.get_mdp()
        liste["voyages_en_cours"]=self.get_voyages_en_cours()
        liste["voyages_passes"]=self.get_voyages_passes()
        return liste
