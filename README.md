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


# Partie B — Gestion des Destinations
**Auteur : Teodora — Membre B**
Projet SAE — Université Sorbonne Paris Nord

---

## Responsabilités

- **Backend** : Création des routes pour ajouter des étapes à un voyage
- **Base de données** : Modélisation de la relation One-to-Many (Voyage → Destinations)
- **DevOps** : Gestion des volumes Docker pour la persistance des données

---

## Fichiers

```
app/
├── models_b.py    → Modèle SQLAlchemy : table 'destinations'
├── schemas_b.py   → Schémas Pydantic  : validation et réponses API
├── crud_b.py      → Fonctions CRUD    : accès base de données
└── routes_b.py    → Routes FastAPI    : router à inclure dans main.py
```

---

## Relation implémentée : One-to-Many

```
voyages (Mathurin — Membre A)       destinations (Teodora — Membre B)
─────────────────────────────       ──────────────────────────────────
voyage_id  PK                  ←──  voyage_id  FK  (ON DELETE CASCADE)
date                                destination_id  PK
lieu                                nom             (obligatoire)
voyage_fini                         localisation    (optionnel)
prix                                categorie       hotel | activite | restaurant
                                    notes           (optionnel)
                                    ordre           position dans l'itinéraire
```

**Un voyage contient plusieurs destinations.**
Si un voyage est supprimé, toutes ses destinations sont supprimées automatiquement (CASCADE).

---

## Routes exposées

| Méthode  | URL                                   | Description                     | Code succès |
|----------|---------------------------------------|---------------------------------|-------------|
| `POST`   | `/voyages/{voyage_id}/destinations/`  | Ajouter une étape à un voyage   | 201         |
| `GET`    | `/voyages/{voyage_id}/destinations/`  | Lister les étapes d'un voyage   | 200         |
| `GET`    | `/destinations/{destination_id}`      | Détail d'une étape              | 200         |
| `PUT`    | `/destinations/{destination_id}`      | Modifier une étape (partiel)    | 200         |
| `DELETE` | `/destinations/{destination_id}`      | Supprimer une étape             | 200         |

---

## Validations (schemas_b.py)

- `nom` : obligatoire, ne peut pas être vide
- `categorie` : doit être `hotel`, `activite` ou `restaurant` (ou null)
- `ordre` : doit être >= 1 (ou null)
- Requête sur `voyage_id` inexistant → **404**
- Données invalides → **422 Validation Error**

---

## Intégration dans le projet commun

### 1. Ajouter le modèle dans `models.py`

```python
from .models_b import Destination  # ← ajouter avant create_all()
```

### 2. Ajouter les routes dans `main.py`

```python
from app.routes_b import router as router_destinations  # ← ajouter
app.include_router(router_destinations)                 # ← ajouter
```

### 3. Ajouter la table dans le script SQL commun

Ajouter après la création de la table `voyages` :

```sql
CREATE TABLE IF NOT EXISTS destinations (
    destination_id  SERIAL PRIMARY KEY,
    nom             VARCHAR(100)  NOT NULL,
    localisation    VARCHAR(100),
    categorie       VARCHAR(50)   CHECK (categorie IN ('hotel', 'activite', 'restaurant')),
    notes           VARCHAR(255),
    ordre           INTEGER       CHECK (ordre >= 1),
    voyage_id       INTEGER       NOT NULL,
    FOREIGN KEY (voyage_id) REFERENCES voyages(voyage_id) ON DELETE CASCADE
);
```

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

**Mise à jour partielle :**
```json
PUT /destinations/1
{
    "notes": "Billet gratuit le premier dimanche du mois."
}
```
Seul le champ `notes` est modifié. Les autres restent inchangés.
