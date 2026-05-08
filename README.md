# ✈️ Projet : Group Trip Planner

Ce projet est réalisé dans le cadre de la **SAE - Développement & Déploiement d'une Application Web RESTful Conteneurisée**.

---

## 1. Objectif Général et Contexte 🌍
Notre application, Group Trip Planner, est une plateforme collaborative conçue pour simplifier l'organisation de voyages à plusieurs. Trop souvent, planifier un voyage en groupe devient complexe à cause de la dispersion des informations. Cette solution permet donc de :

* **Centraliser l'itinéraire** : Créer un voyage et y ajouter différentes étapes ou destinations (hôtels, activités, restaurants).
* **Gérer les participants** : Inviter des amis à rejoindre un voyage spécifique pour que tout le monde ait accès au même programme.
* **Suivre le budget** : Associer un plan budgétaire à chaque voyage pour garder un œil sur les dépenses prévues.

L'idée est d'offrir une interface unique où chaque membre du groupe peut consulter et modifier les détails du séjour en temps réel.

---

## 2. Choix Techniques 🛠️
Notre stack technique respecte les contraintes imposées par le sujet :

* **Backend** : Python avec le framework FastAPI.
* **Base de données** : PostgreSQL (Base de données relationnelle).
* **ORM** : SQLAlchemy (obligatoire pour la persistance des données).
* **Frontend** : HTML5, CSS3 et JavaScript vanilla (ES6+) — sans framework, sans build step.
* **Infrastructure** : Conteneurisation totale via Docker et orchestration via Docker Compose.

### Front-end : technologies utilisées
* **HTML5 sémantique** (`<aside>`, `<main>`, `<section>`, `<nav>`)
* **CSS3 moderne** : variables CSS, Grid, Flexbox, `@keyframes`, `backdrop-filter`, `@media` queries
* **JavaScript ES6+ vanilla** : Fetch API, async/await, localStorage, DOM API, `Intl.NumberFormat`
* **Google Fonts** : Fraunces (display serif), Inter (body sans-serif), JetBrains Mono (monospace)
* **Aucune dépendance npm**, aucun bundler, aucun framework — un seul `index.html`, un seul `styles.css`, un seul `app.js`

---

## 3. Modélisation de la Base de Données (ORM) 📊
Nous implémentons les trois types de relations suivants dans notre code et notre schéma SQL :

| Type de Relation | Description |
| :--- | :--- |
| **One-to-One** | Un Voyage possède un seul Plan Budgétaire (Budget plan). |
| **One-to-Many** | Un Voyage contient plusieurs Destinations (Étapes du trajet). |
| **Many-to-Many** | Les Utilisateurs participent à plusieurs Voyages, et un voyage regroupe plusieurs utilisateurs. |

---

## 4. Guide d'Exécution avec Docker 🚀
Cette application est entièrement conteneurisée. Pour la lancer, vous n'avez pas besoin d'installer Python, Node.js ou PostgreSQL sur votre machine, seulement **Docker** et **Docker Compose**.

#### 1. Prérequis
* Docker installé sur votre machine.
* Docker Compose.

#### 2. Lancement de l'application
Depuis la racine du projet (là où se trouve le fichier `docker-compose.yml`), exécutez :
```bash
docker-compose up --build
```

Pour arrêter et nettoyer les containers :
```bash
docker-compose down
```

Pour repartir de zéro (réinitialise aussi la base de données) :
```bash
docker-compose down -v && docker-compose up --build
```

---

## 5. Accès à l'Application 🌐

Une seule URL donne accès à tout — le front-end et l'API sont servis par le même container.

| Page | URL |
| :--- | :--- |
| **Front-end (Console)** | [http://localhost:8080](http://localhost:8080) |
| **API JSON (welcome)** | [http://localhost:8080/api](http://localhost:8080/api) |
| **Swagger UI** | [http://localhost:8080/docs](http://localhost:8080/docs) |
| **Redoc** | [http://localhost:8080/redoc](http://localhost:8080/redoc) |

---

## 6. Architecture du Projet 🏗️
```text
.
├── app/
│   ├── crud.py            # Logique pour les opérations CRUD
│   ├── database.py        # Configuration et session de la base de données
│   ├── main.py            # Point d'entrée FastAPI (CORS + montage du front-end)
│   ├── models.py          # Définition des modèles ORM (SQLAlchemy)
│   ├── routes_b.py        # Définition des points de terminaison API
│   ├── schemas.py         # Modèles Pydantic pour la validation des données
│   └── verification.py    # Utilitaires de vérification/sécurité
├── frontend/              # Interface web (servie par FastAPI)
│   ├── index.html         # Structure de la page
│   ├── styles.css         # Thème éditorial (Fraunces + Inter)
│   └── app.js             # Logique cliente : appels API, navigation, formulaires
├── Dockerfile             # Image Docker (Python + frontend embarqué)
├── docker-compose.yml     # Orchestration de l'API et de PostgreSQL
├── init.sql               # Script SQL d'initialisation de la base
├── requirements.txt       # Dépendances Python (FastAPI, SQLAlchemy, etc.)
└── README.md              # Documentation du projet
```

---

## 7. Documentation de l'API 🚀

L'API fournit 27 points de terminaison (endpoints) répartis sur 5 modules. Tous respectent les standards REST (GET, POST, PUT, DELETE).

### 7.1 Général
| Méthode | URL    | Description                |
| :------ | :----- | :------------------------- |
| `GET`   | `/api` | Message d'accueil et schéma |

### 7.2 Utilisateurs
| Méthode  | URL                              | Description                 |
| :------- | :------------------------------- | :-------------------------- |
| `POST`   | `/utilisateurs`                  | Créer un utilisateur        |
| `GET`    | `/utilisateurs`                  | Lister tous les utilisateurs |
| `GET`    | `/utilisateurs/all/{email}`      | Détails d'un utilisateur    |
| `GET`    | `/utilisateurs/nom/{email}`      | Récupérer le nom            |
| `GET`    | `/utilisateurs/prenom/{email}`   | Récupérer le prénom         |
| `GET`    | `/utilisateurs/age/{email}`      | Récupérer l'âge             |
| `PUT`    | `/utilisateurs/{email}`          | Mettre à jour un utilisateur |
| `DELETE` | `/utilisateurs/{email}`          | Supprimer un utilisateur    |

### 7.3 Voyages
| Méthode  | URL                              | Description                 |
| :------- | :------------------------------- | :-------------------------- |
| `POST`   | `/voyages`                       | Créer un voyage             |
| `GET`    | `/voyages`                       | Lister tous les voyages     |
| `GET`    | `/voyages/all/{voyage_id}`       | Détails d'un voyage         |
| `GET`    | `/voyages/lieu/{voyage_id}`      | Récupérer le lieu           |
| `GET`    | `/voyages/prix/{voyage_id}`      | Récupérer le prix           |
| `GET`    | `/voyages/voyage_fini/{voyage_id}` | Récupérer le statut       |
| `PUT`    | `/voyages/{voyage_id}`           | Mettre à jour un voyage     |
| `DELETE` | `/voyages/{voyage_id}`           | Supprimer un voyage         |

### 7.4 Relations (Many-to-Many)
| Méthode  | URL                                         | Description                       |
| :------- | :------------------------------------------ | :-------------------------------- |
| `POST`   | `/relations`                                | Lier un utilisateur à un voyage   |
| `GET`    | `/relations`                                | Lister toutes les relations       |
| `GET`    | `/relations/voyage_id/{utilisateur_id}`     | Voyages d'un utilisateur          |
| `GET`    | `/relations/utilisateur_id/{voyage_id}`     | Utilisateurs d'un voyage          |
| `DELETE` | `/relations`                                | Supprimer une relation            |

### 7.5 Destinations (One-to-Many)
| Méthode  | URL                                       | Description               | Code succès |
| :------- | :---------------------------------------- | :------------------------ | :---------- |
| `POST`   | `/voyages/{voyage_id}/destinations/`      | Ajouter une étape         | 201         |
| `GET`    | `/voyages/{voyage_id}/destinations/`      | Lister les étapes         | 200         |
| `GET`    | `/destinations/{destination_id}`          | Détail d'une étape        | 200         |
| `PUT`    | `/destinations/{destination_id}`          | Modifier une étape        | 200         |
| `DELETE` | `/destinations/{destination_id}`          | Supprimer une étape       | 200         |

### 7.6 Budget (One-to-One)
| Méthode  | URL                              | Description                |
| :------- | :------------------------------- | :------------------------- |
| `POST`   | `/voyages/{trip_id}/budget`      | Créer un budget            |
| `GET`    | `/voyages/{trip_id}/budget`      | Récupérer le budget        |
| `PUT`    | `/voyages/{trip_id}/budget`      | Mettre à jour le budget    |

---

## 8. Exemple d'utilisation

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

---

## 9. Front-end 🎨

L'interface web est servie directement par FastAPI grâce à `StaticFiles`, et elle communique avec l'API via la même origine (pas besoin de configurer une URL externe).

### Sections de la console
1. **Tableau de bord** — statistiques globales et derniers voyages enregistrés
2. **Utilisateurs** — création, édition champ par champ, suppression
3. **Voyages** — CRUD complet, bascule de statut "terminé/à venir" en un clic
4. **Destinations** — gestion des étapes par voyage avec catégories (hôtel/activité/restaurant)
5. **Budget** — barre de progression visuelle avec alerte de dépassement
6. **Relations** — liaison utilisateur ↔ voyage avec sélecteurs croisés

### Fonctionnalités techniques
* **Détection automatique de l'API** : `location.origin` par défaut, modifiable via la sidebar
* **Health-check live** : ping de `/api` toutes les 30 secondes, indicateur vert/rouge
* **Toasts d'erreur** : affichage des messages `detail` retournés par FastAPI (validation Pydantic incluse)
* **Persistance utilisateur** : l'URL de l'API est sauvegardée dans `localStorage`
* **Responsive** : adaptation mobile sous 900px et 700px

---

## 10. Modifications clés pour la connexion front ↔ back 🔌

Trois modifications ont été nécessaires pour faire fonctionner le front-end et le back-end ensemble dans un seul container :

### `app/main.py`
* Ajout de `CORSMiddleware` pour autoriser les appels JavaScript du navigateur
* Ajout de `StaticFiles` mount sur `/` pour servir le dossier `frontend/`
* Déplacement de la route `GET /` vers `GET /api` (pour ne pas entrer en conflit avec le mount)

### `Dockerfile`
* Ajout de `COPY ./frontend /code/frontend` pour embarquer l'interface web dans l'image

### `docker-compose.yml`
* Remplacement de `image: ztmprosae/group-trip-planner:latest` par `build: .` pour rebuilder localement avec les modifications

---

## 11. Publication Docker Hub 🐳

* **Lien vers l'image :** [https://hub.docker.com/r/ztmprosae/group-trip-planner](https://hub.docker.com/r/ztmprosae/group-trip-planner)
* **Récupérer l'image :**
  ```bash
  docker pull ztmprosae/group-trip-planner:latest
  ```
* **Publier une nouvelle version :**
  ```bash
  docker login
  docker build -t ztmprosae/group-trip-planner:latest .
  docker push ztmprosae/group-trip-planner:latest
  ```

---

## 12. Membres de l'équipe 👥

* **Mathurin**
* **Teodora**
* **Zeynab**
