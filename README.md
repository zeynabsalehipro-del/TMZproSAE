# Projet-Group Trip Planner
1. Objectif Général et Contexte
Notre application, Group Trip Planner, est une plateforme collaborative conçue pour simplifier l'organisation de voyages à plusieurs. Trop souvent, planifier un voyage en groupe devient complexe à cause de la dispersion des informations. Cette solution permet donc de :
Centraliser l'itinéraire : Créer un voyage et y ajouter différentes étapes ou destinations (hôtels, activités, restaurants).
Gérer les participants : Inviter des amis à rejoindre un voyage spécifique pour que tout le monde ait accès au même programme.
Suivre le budget : Associer un plan budgétaire à chaque voyage pour garder un œil sur les dépenses prévues.
L'idée est d'offrir une interface unique où chaque membre du groupe peut consulter et modifier les détails du séjour en temps réel.

2. Choix Techniques
Notre stack technique :
Backend : Python avec le framework FastAPI (ou Flask).
Base de données : PostgreSQL (Base de données relationnelle).
ORM : SQLAlchemy (obligatoire pour la persistance des données).
Infrastructure : Conteneurisation totale via Docker et orchestration via Docker Compose.
3. Modélisation de la Base de Données (ORM)
Nous devons implémenter au moins les trois types de relations suivants dans notre code et notre schéma SQL:
One-to-One : Un Voyage possède un seul Plan Budgétaire (Budget plan).
One-to-Many : Un Voyage contient plusieurs Destinations (Étapes du trajet).
Many-to-Many : Les Utilisateurs participent à plusieurs Voyages, et un voyage regroupe plusieurs utilisateurs.
4. Livrables Attendus (Check-list pour l'équipe)
Pour valider l'évaluation, notre dépôt GitHub doit contenir :
Code Source : L'intégralité du backend Python.
Docker : Un fichier docker-compose.yml fonctionnel pour lancer l'API et la DB simultanément.
Données : Un script SQL pour importer un jeu de données de test minimal.
Documentation : Un fichier README.md expliquant le contexte, l'architecture et les routes de l'API.
Docker Hub : Une image Docker de notre API publiée sur Docker Hub.
5. Organisation et Soutenance
Soutenance : Présentation orale de 15 minutes suivie de 5 minutes de questions.
Démonstration : Nous devons montrer le fonctionnement de l'API via Postman ou Swagger.
Évaluation par les pairs : 30% de la note finale dépendra de l'évaluation anonyme faite par nos camarades.
6. Répartition des tâches
1. Membre A : Gestion des Utilisateurs & Infrastructure de Base
Backend : Création de l'API pour l'inscription et la connexion (Auth).
Base de données : Modélisation de la relation Many-to-Many (Utilisateurs <-> Voyages).
Docker : Configuration initiale du Dockerfile et de la base de données PostgreSQL.
2. Membre B : Gestion des Voyages & Destinations
Backend : Création des routes pour créer un voyage et ajouter des étapes.
Base de données : Modélisation de la relation One-to-Many (Voyage -> Destinations).
DevOps : Publication de l'image sur Docker Hub et gestion des Volumes pour les données.
3. Membre C : Gestion du Budget & Qualité du Projet
Backend : Création de l'API pour le suivi des dépenses du voyage.
Base de données : Modélisation de la relation One-to-One (Voyage -> Budget).
Documentation & Tests : Configuration de Swagger, rédaction du README.md final et préparation de la soutenance.

