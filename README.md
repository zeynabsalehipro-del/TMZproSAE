# ✈️ Projet : Group Trip Planner

[cite_start]Ce projet est réalisé dans le cadre de la **SAE - Développement & Déploiement d'une Application Web RESTful Conteneurisée**. [cite: 3, 4, 5]

---

## 1. Objectif Général et Context 🌍
[cite_start]**Group Trip Planner** est une plateforme collaborative conçue pour simplifier l'organisation de voyages à plusieurs. [cite: 55] Cette solution permet de :

* **Centraliser l'itinéraire** : Créer un voyage et y ajouter différentes étapes (hôtels, activités, restaurants).
* **Gérer les participants** : Inviter des amis à rejoindre un voyage pour un accès partagé au programme.
* **Suivre le budget** : Associer un plan budgétaire à chaque voyage pour surveiller les dépenses.

---

## 2. Choix Techniques 🛠️
[cite_start]Notre stack technique respecte les contraintes imposées par le sujet : [cite: 12]

* [cite_start]**Backend** : Python avec le framework **FastAPI** (ou Flask). [cite: 14]
* [cite_start]**Base de données** : **PostgreSQL** (Relationnelle). [cite: 15]
* [cite_start]**ORM** : **SQLAlchemy** (obligatoire pour la persistance). [cite: 18, 19]
* [cite_start]**Infrastructure** : Conteneurisation via **Docker** et orchestration via **Docker Compose**. [cite: 16, 17]

---

## 3. Modélisation de la Base de Données (ORM) 📊
[cite_start]Nous implémentons les trois types de relations obligatoires : [cite: 20]

| Type de Relation | Description |
| :--- | :--- |
| **One-to-One** | [cite_start]Un Voyage possède un seul Plan Budgétaire. [cite: 21] |
| **One-to-Many** | [cite_start]Un Voyage contient plusieurs Destinations (étapes). [cite: 22] |
| **Many-to-Many** | [cite_start]Les Utilisateurs participent à plusieurs Voyages. [cite: 23] |

---

## 4. Livrables Attendus ✅
[cite_start]Conformément aux exigences, le dépôt contient : [cite: 47]

- [x] [cite_start]**Code Source** : Intégralیت du backend Python. [cite: 48]
- [x] [cite_start]**Docker** : Fichier `docker-compose.yml` fonctionnel. [cite: 50]
- [x] [cite_start]**Données** : Script SQL d'importation pour les tests. [cite: 51]
- [x] [cite_start]**Documentation** : Ce fichier README détaillant l'architecture et les routes. [cite: 49]
- [x] [cite_start]**Docker Hub** : Image publiée sur Docker Hub. [cite: 63]

---

## 5. Répartition des Tâches 👥

### 👤 Membre A : Gestion des Utilisateurs & Infrastructure
* **Backend** : API pour l'inscription et la connexion (Auth).
* **Base de données** : Relation Many-to-Many (Utilisateurs ↔ Voyages).
* **Docker** : Configuration du `Dockerfile` et de PostgreSQL.

### 👤 Membre B : Gestion des Voyages & Destinations
* **Backend** : Routes pour créer un voyage et ajouter des étapes.
* **Base de données** : Relation One-to-Many (Voyage → Destinations).
* [cite_start]**DevOps** : Publication sur **Docker Hub** et gestion des volumes. [cite: 63]

### 👤 Membre C : Gestion du Budget & Qualité
* **Backend** : API pour le suivi des dépenses.
* **Base de données** : Relation One-to-One (Voyage → Budget).
* [cite_start]**Qualité** : Configuration de Swagger, README final et préparation de la soutenance. [cite: 27, 34]

---

## 6. Installation et Lancement 🚀
[cite_start]Pour lancer l'application en local avec Docker Compose : [cite: 56]

```bash
docker-compose up --build
