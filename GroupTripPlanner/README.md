# ✈️ Projet : Group Trip Planner

Ce projet est réalisé dans le cadre de la **SAE - Développement & Déploiement d'une Application Web RESTful Conteneurisée**. 

---

## 1. Objectif Général et Context 🌍
Notre application, Group Trip Planner, est une plateforme collaborative conçue pour simplifier l'organisation de voyages à plusieurs. Trop souvent, planifier un voyage en groupe devient complexe à cause de la dispersion des informations. Cette solution permet donc de :

* **Centraliser l'itinéraire** : Créer un voyage et y ajouter différentes étapes ou destinations (hôtels, activités, restaurants).
* **Gérer les participants** : Inviter des amis à rejoindre un voyage spécifique pour que tout le monde ait accès au même programme.
* **Suivre le budget** : Associer un plan budgétaire à chaque voyage pour garder un œil sur les dépenses prévues.
L'idée est d'offrir une interface unique où chaque membre du groupe peut consulter et modifier les détails du séjour en temps réel.
---

## 2. Choix Techniques 🛠️
Notre stack technique respecte les contraintes imposées par le sujet :

* **Backend** : Python avec le framework FastAPI (ou Flask).
* **Base de données** : PostgreSQL (Base de données relationnelle).
* **ORM** : SQLAlchemy (obligatoire pour la persistance des données).
* **Infrastructure** :  Conteneurisation totale via Docker et orchestration via Docker Compose.

---

## 3. Modélisation de la Base de Données (ORM) 📊
Nous devons implémenter au moins les trois types de relations suivants dans notre code et notre schéma SQL:

| Type de Relation | Description |
| :--- | :--- |
| **One-to-One** | Un Voyage possède un seul Plan Budgétaire (Budget plan). |
| **One-to-Many** | Un Voyage contient plusieurs Destinations (Étapes du trajet). |
| **Many-to-Many** | Les Utilisateurs participent à plusieurs Voyages, et un voyage regroupe plusieurs utilisateurs.|

---

## 4. Guide d'Exécution avec Docker🚀
Cette application est entièrement conteneurisée. Pour la lancer, vous n'avez pas besoin d'installer Python ou PostgreSQL sur votre machine, seulement **Docker** et **Docker Compose**.

#### 1. Prérequis
*   Docker installé sur votre machine.
*   Docker Compose.

#### 2. Lancement de l'application
Depuis la racine du projet (là où se trouve le fichier `docker-compose.yml`), exécutez la commande suivante dans votre terminal:
```bash
docker-compose up --build
```

---
## 5. Accès à la Documentation Interactive (Swagger)

*   **Swagger UI** : Accédez à [http://localhost:8080/docs](http://localhost:8080/docs)
*   **Redoc** : Accédez à [http://localhost:8080/redoc](http://localhost:8080/redoc)


# 6. Architecture du Projet 🏗️
```text
.
├── app/
│   ├── crud.py            # Logique pour les opérations CRUD
│   ├── database.py        # Configuration et session de la base de données
│   ├── main.py            # Point d'entrée de l'application FastAPI
│   ├── models.py          # Définition des modèles ORM (SQLAlchemy)
│   ├── routes_b.py        # Définition des points de terminaison (endpoints) API
│   ├── schemas.py         # Modèles Pydantic pour la validation des données
│   └── verification.py    # Utilitaires de vérification/sécurité
├── Dockerfile             # Fichier de configuration pour l'image Docker de l'API
├── docker-compose.yml     # Orchestration de l'API et de la base de données PostgreSQL
├── init.sql               # Script SQL pour initialiser la base de données
├── requirements.txt       # Liste des dépendances Python (FastAPI, SQLAlchemy, etc.)
├── .gitignore             # Fichiers à exclure du suivi Git
└── README.md              # Documentation du projet
```
---

---

## 7. Documentation de l'API 🚀

L'API fournit plusieurs points de terminaison (endpoints) pour gérer les voyages et les destinations. Nous avons respecté les standards REST (GET, POST, PUT, DELETE) pour assurer une interaction fluide avec les données.

### Routes exposées

| Méthode  | URL                                   | Description                     | Code succès |
|----------|---------------------------------------|---------------------------------|-------------|
| `POST`   | `/voyages/{voyage_id}/destinations/`  | Ajouter une étape à un voyage   | 201         |
| `GET`    | `/voyages/{voyage_id}/destinations/`  | Lister les étapes d'un voyage   | 200         |
| `GET`    | `/destinations/{destination_id}`      | Détail d'une étape              | 200         |
| `PUT`    | `/destinations/{destination_id}`      | Modifier une étape (partiel)    | 200         |
| `DELETE` | `/destinations/{destination_id}`      | Supprimer une étape             | 200         |

---

## Exemple d'utilisation

**Créer une destination :**

```json
POST /voyages/1/destinations/
{
    "nom": "Colisée",
    "localisation": "Rome, Italie",
    "categorie": "activite",
    "notes": "Réserver les billets en avance.",
    "ordre": 1
}
```

**Réponse (201) :**
```json
{
    "destination_id": 1,
    "nom": "Colisée",
    "localisation": "Rome, Italie",
    "categorie": "activite",
    "notes": "Réserver les billets en avance.",
    "ordre": 1,
    "voyage_id": 1
}
```

